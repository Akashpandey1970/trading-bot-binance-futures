import streamlit as st
import os
import time
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import validate_inputs

# 1. Page Configuration for a striking, dark trading desk look
st.set_page_config(
    page_title="Primetrade.ai | Order Execution Desk",
    page_icon="📈",
    layout="wide"
)

# 2. Injecting precise button styling updates safely
st.markdown("""
    <style>
    h1, h2, h3 { color: #f0b90b !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button {
        background-color: #f0b90b !important; color: #000000 !important;
        font-weight: bold !important; font-size: 16px !important;
        border-radius: 6px !important; width: 100%; height: 48px;
        border: none !important; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #f8d147 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize and Check API Client State securely
@st.cache_resource
def get_bot_manager():
    try:
        client_wrapper = BinanceFuturesClient()
        return OrderManager(client_wrapper), None
    except Exception as e:
        return None, str(e)

manager, init_error = get_bot_manager()

# --- HEADER LAYOUT ---
st.title("📈 Primetrade.ai — Advanced Futures Order Desk")
st.caption("Enterprise-grade Binance Futures Testnet (USDT-M) Execution Module")
st.markdown("---")

# --- MAIN DASHBOARD BODY Split into 2 Interactive Columns ---
col_left, col_right = st.columns([1.2, 1.8], gap="large")

with col_left:
    st.subheader("🎛️ Order Configuration")
    
    # Using native border containers eliminates layout glitching completely
    with st.container(border=True):
        symbol = st.text_input("Symbol Ticker", value="BTCUSDT", placeholder="e.g. ETHUSDT").upper().strip()
        
        col_side, col_type = st.columns(2)
        with col_side:
            side = st.selectbox("Action Side", ["BUY", "SELL"])
        with col_type:
            order_type = st.selectbox("Order Type Strategy", ["MARKET", "LIMIT", "STOP_LIMIT"])
            
        quantity = st.number_input("Order Quantity", min_value=0.000, value=0.010, step=0.001, format="%.3f")
        
        price = None
        stop_price = None
        
        if order_type in ["LIMIT", "STOP_LIMIT"]:
            price = st.number_input("Limit Execution Price ($)", min_value=0.0, value=30000.0, step=0.1)
        if order_type == "STOP_LIMIT":
            stop_price = st.number_input("Activation Trigger Price ($)", min_value=0.0, value=30500.0, step=0.1)
            
        st.write("") # Visual breathing room
        submit_order = st.button("🚀 Transmit Order Payload")
        
        if submit_order:
            try:
                validate_inputs(symbol, side, order_type, quantity, price, stop_price)
                
                if init_error:
                    st.error(f"Execution Blocked: Server authentication failed. {init_error}")
                else:
                    with st.spinner("Broadcasting to Binance Match Engine..."):
                        result = manager.place_futures_order(
                            symbol=symbol, side=side, order_type=order_type,
                            quantity=quantity, price=price, stop_price=stop_price
                        )
                        
                    if result["success"]:
                        res = result["data"]
                        st.balloons()
                        st.success("🎉 Transaction Confirmed on Testnet Server Ledger!")
                        
                        with st.container(border=True):
                            m1, m2 = st.columns(2)
                            m1.metric("Order ID", res.get('orderId'))
                            m2.metric("Status State", res.get('status'))
                            m3, m4 = st.columns(2)
                            m3.metric("Filled Qty", res.get('executedQty'))
                            m4.metric("Avg Execution Price", res.get('avgPrice', 'N/A'))
                    else:
                        st.error(f"❌ Exchange Rejected Request:\n{result['error']}")
                        
            except ValueError as val_err:
                st.warning(f"⚠️ Pre-flight Input Violation: {val_err}")

with col_right:
    st.subheader("🖥️ Live Telemetry & System Infrastructure Logs")
    
    with st.container(border=True):
        if init_error:
            st.markdown("🔴 **Gateway Connection Status:** `DISCONNECTED / AUTH_ERROR`")
        else:
            st.markdown("🟢 **Gateway Connection Status:** `CONNECTED (BINANCE F-TESTNET)`")
    
    st.markdown("**Active Trace Streams (`logs/trading_bot.log`)**")
    
    log_file_path = os.path.join(os.path.dirname(__file__), "logs", "trading_bot.log")
    
    with st.container(border=True):
        log_box = st.empty()
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as f:
                lines = f.readlines()
                log_display = "".join(lines[-15:])
                log_box.code(log_display, language="text")
        else:
            log_box.info("Awaiting initial transaction stream pipeline initialization...")
        
    if st.button("🔄 Force Refresh Log Trails"):
        st.rerun()