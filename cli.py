import argparse
import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import (
    validate_symbol, validate_side, validate_order_type, 
    validate_quantity, validate_price
)
from bot.logging_config import logger

console = Console()

def setup_parser():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], type=str.upper, help="Order side (BUY or SELL)")
    parser.add_argument("--order_type", required=True, choices=["MARKET", "LIMIT"], type=str.upper, help="Order type (MARKET or LIMIT)")
    parser.add_argument("--quantity", required=True, help="Amount to trade")
    parser.add_argument("--price", help="Required for LIMIT orders")
    return parser

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        console.print("[red]Error: API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in the .env file.[/red]")
        sys.exit(1)

    parser = setup_parser()
    args = parser.parse_args()

    # Input Validation
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
    except ValueError as e:
        console.print(f"[red]Input Validation Error: {e}[/red]")
        sys.exit(1)

    # 4. Print clear output:
    # - order request summary
    summary_msg = (
        f"[yellow]Symbol:[/yellow]    {symbol}\n"
        f"[yellow]Side:[/yellow]      {side}\n"
        f"[yellow]Type:[/yellow]      {order_type}\n"
        f"[yellow]Quantity:[/yellow]  {quantity}"
    )
    if price:
        summary_msg += f"\n[yellow]Price:[/yellow]     {price}"
        
    console.print(Panel(summary_msg, title="[bold white]1. Order Request Summary[/bold white]", border_style="cyan"))

    # Initialize client and manager
    client = BinanceFuturesClient(api_key, api_secret)
    order_manager = OrderManager(client)

    # Place Order
    console.print("\n[bold]Sending request to Binance Futures Testnet...[/bold]")
    try:
        response = order_manager.place_order(symbol, side, order_type, quantity, price)
        
        # - success/failure message
        console.print("\n[bold green]✅ SUCCESS: Order has been placed successfully![/bold green]")

        # - order response details (orderId, status, executedQty, avgPrice if available)
        avg_price = response.get('avgPrice', '0.00')
        if not avg_price or float(avg_price) == 0:
            avg_price = "Market"

        response_msg = (
            f"[green]Order ID:[/green]     {response.get('orderId')}\n"
            f"[green]Status:[/green]       {response.get('status')}\n"
            f"[green]Executed Qty:[/green] {response.get('executedQty')}\n"
            f"[green]Avg Price:[/green]    {avg_price}"
        )
            
        console.print(Panel(response_msg, title="[bold white]2. Order Response Details[/bold white]", border_style="green"))
        
    except Exception as e:
        console.print("\n[bold red]❌ FAILURE: Order placement failed![/bold red]")
        console.print(Panel(f"[red]{str(e)}[/red]", title="[bold white]Error Details[/bold white]", border_style="red"))
        sys.exit(1)

if __name__ == "__main__":
    main()
