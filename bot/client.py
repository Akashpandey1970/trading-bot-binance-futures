import os
import time
from binance import Client
from bot.logging_config import setup_logging

logger = setup_logging()

class BinanceFuturesClient:
    def __init__(self):
        raw_key = os.getenv("BINANCE_TESTNET_API_KEY", "")
        raw_secret = os.getenv("BINANCE_TESTNET_API_SECRET", "")
        
        self.api_key = raw_key.strip()
        self.api_secret = raw_secret.strip()
        
        if not self.api_key or not self.api_secret:
            logger.error("API credentials missing from environment.")
            raise ValueError("Please export BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET.")
        
        try:
            # 1. Initialize the client wrapper mapping
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            
            # 2. ✨ FORCE FUTURES TIMESTAMPS: Fetch the exact current time from the Futures Testnet server
            logger.info("Synchronizing local client clock with Binance Futures Testnet Server...")
            futures_server_time = self.client.futures_time()['serverTime']
            
            # 3. Overwrite python-binance's internal tracking offset with the futures calculation
            local_time_ms = int(time.time() * 1000)
            self.client.timestamp_offset = futures_server_time - local_time_ms
            
            logger.info(f"Clock synchronization complete. Applied Offset: {self.client.timestamp_offset}ms")
            logger.info("Binance Futures Testnet Client successfully established.")
        except Exception as e:
            logger.error(f"Failed initialization: {e}")
            raise