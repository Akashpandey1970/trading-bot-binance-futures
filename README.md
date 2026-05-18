# Simplified Binance Futures Testnet Trading Bot

A production-ready, modular Python CLI application built to interact with the Binance Futures Testnet (USDT-M). This application allows users to safely validate and place Market, Limit, and Stop-Limit orders without risking real capital.

## 🌟 Key Features
*   **Fully Modular Architecture:** Separate layers for CLI parsing, input pre-flight validation, and API client wrappers.
*   **Production-Grade Logging:** Dual-stream logging. Clean, human-readable summaries output directly to the terminal, while precise payload/response JSON traces are piped to `logs/trading_bot.log`.
*   **Bonus Objective Complete:** Implemented full support for `STOP_LIMIT` orders alongside standard Market and Limit types.
*   **Secure Credential Management:** Zero hardcoded secrets; utilizes system environment variables.

---

## 📂 Project Structure
```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py          # Tracks connection to Testnet
│   ├── orders.py          # Handles Market/Limit/Stop-Limit execution
│   ├── validators.py      # Pre-flight parameter validation
│   └── logging_config.py  # Coordinates logging setup
│
├── logs/
│   └── trading_bot.log    # Generated runtime execution logs
│
├── cli.py                 # Core CLI runtime gateway
├── requirements.txt       # Project dependencies
└── README.md              # Setup and execution manual