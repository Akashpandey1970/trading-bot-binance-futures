from binance.exceptions import BinanceAPIException
from bot.client import BinanceFuturesClient
from bot.logging_config import setup_logging

logger = setup_logging()

class OrderManager:
    def __init__(self, client_wrapper: BinanceFuturesClient):
        self.client = client_wrapper.client

    def place_futures_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "recvWindow": 60000  # ✨ ADD THIS: Grants a 60-second processing window cushion
        }
        
        # Adjust logic and parameters depending on custom trading choices
        if order_type == "LIMIT":
            params["price"] = str(price)
            params["timeInForce"] = "GTC"  # Good 'Til Cancelled
        elif order_type == "STOP_LIMIT":
            params["type"] = "STOP"
            params["price"] = str(price)
            params["stopPrice"] = str(stop_price)
            params["timeInForce"] = "GTC"

        logger.info(f"Sending API Payload: {params}")
        
        try:
            # Execute trade against the USDT-M Futures endpoint
            response = self.client.futures_create_order(**params)
            logger.info(f"Execution Successful. Server Response: {response}")
            return {"success": True, "data": response}
            
        except BinanceAPIException as e:
            err = f"API Error Code {e.code}: {e.message}"
            logger.error(err)
            return {"success": False, "error": err}
        except Exception as e:
            err = f"Network Connection / Transport Exception: {str(e)}"
            logger.error(err)
            return {"success": False, "error": err}