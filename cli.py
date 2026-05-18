import argparse
import sys
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import validate_inputs
from bot.logging_config import setup_logging

logger = setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Primetrade.ai Bot Interface")
    parser.add_argument("--symbol", type=str, required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"])
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float, help="Price for LIMIT / STOP_LIMIT")
    parser.add_argument("--stop_price", type=float, help="Trigger Price for STOP_LIMIT")

    args = parser.parse_args()

    # Pre-flight data evaluation
    try:
        validate_inputs(args.symbol, args.side, args.type, args.quantity, args.price, args.stop_price)
    except ValueError as e:
        print(f"\n❌ Validation Failure: {e}")
        sys.exit(1)

    print("\n==========================================")
    print("📋 ORDER REQUEST PROFILE SUMMARY")
    print("==========================================")
    print(f"Symbol:     {args.symbol.upper()}")
    print(f"Side:       {args.side.upper()}")
    print(f"Type:       {args.type.upper()}")
    print(f"Quantity:   {args.quantity}")
    if args.price: print(f"Price:      {args.price}")
    if args.stop_price: print(f"Stop Price: {args.stop_price}")
    print("==========================================\n")

    try:
        client_wrapper = BinanceFuturesClient()
        manager = OrderManager(client_wrapper)
        
        print("📡 Broadcasting order out to Binance Futures Testnet...")
        result = manager.place_futures_order(
            symbol=args.symbol, side=args.side, order_type=args.type,
            quantity=args.quantity, price=args.price, stop_price=args.stop_price
        )
        
        if result["success"]:
            res = result["data"]
            print("\n✅ ORDER PROCESSED SUCCESSFULLY")
            print("------------------------------------------")
            print(f"Order ID:      {res.get('orderId')}")
            print(f"Status:        {res.get('status')}")
            print(f"Executed Qty:  {res.get('executedQty')}")
            print(f"Avg Price:     {res.get('avgPrice', 'N/A')}")
            print("------------------------------------------")
        else:
            print(f"\n❌ TRANSACTION REJECTED")
            print(f"Reason: {result['error']}")
            
    except Exception as e:
        print(f"\n❌ System Interruption Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()