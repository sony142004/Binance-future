from bot.client import BinanceFuturesClient
from bot.logging_config import logger

class OrderManager:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC" # Good Till Cancel

        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}" + (f" at {price}" if price else ""))
        
        try:
            response = self.client._request("POST", endpoint, params)
            logger.info(f"Order success: ID {response.get('orderId')}, Status {response.get('status')}")
            return response
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            raise
