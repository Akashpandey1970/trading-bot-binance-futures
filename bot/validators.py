def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string (e.g., BTCUSDT).")
    
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be either BUY or SELL.")
        
    if order_type.upper() not in ["MARKET", "LIMIT", "STOP_LIMIT"]:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_LIMIT.")
        
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
        
    if order_type.upper() in ["LIMIT", "STOP_LIMIT"] and (price is None or price <= 0):
        raise ValueError("Price is required and must be greater than 0 for LIMIT or STOP_LIMIT orders.")
        
    if order_type.upper() == "STOP_LIMIT" and (stop_price is None or stop_price <= 0):
        raise ValueError("Stop Price is required and must be greater than 0 for STOP_LIMIT orders.")