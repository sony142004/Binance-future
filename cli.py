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

    # Output order request summary
    summary_text = (
        f"Symbol: [bold cyan]{symbol}[/bold cyan]\n"
        f"Side: [bold cyan]{side}[/bold cyan]\n"
        f"Type: [bold cyan]{order_type}[/bold cyan]\n"
        f"Quantity: [bold cyan]{quantity}[/bold cyan]"
    )
    if order_type == "LIMIT":
        summary_text += f"\nPrice: [bold cyan]{price}[/bold cyan]"
        
    console.print(Panel(summary_text, title="[yellow]Order Request Summary[/yellow]"))

    # Initialize client and manager
    client = BinanceFuturesClient(api_key, api_secret)
    order_manager = OrderManager(client)

    # Place Order
    console.print("Sending request to Binance Futures Testnet...")
    try:
        response = order_manager.place_order(symbol, side, order_type, quantity, price)
        
        success_msg = (
            f"[bold green]Order Placed Successfully![/bold green]\n\n"
            f"Order ID: [cyan]{response.get('orderId')}[/cyan]\n"
            f"Status: [cyan]{response.get('status')}[/cyan]\n"
            f"Executed Qty: [cyan]{response.get('executedQty')}[/cyan]\n"
        )
        if response.get('avgPrice') and float(response.get('avgPrice')) > 0:
            success_msg += f"Avg Price: [cyan]{response.get('avgPrice')}[/cyan]\n"
            
        console.print(Panel(success_msg, title="[green]Order Response[/green]"))
        
    except Exception as e:
        console.print(Panel(f"[red]{e}[/red]", title="[red]Order Failed[/red]"))
        sys.exit(1)

if __name__ == "__main__":
    main()
