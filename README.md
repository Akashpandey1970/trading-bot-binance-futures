# Advanced Binance Futures Testnet Trading Desk

An industry-level, modular Python application designed to interface with the Binance Futures Testnet (USDT-M). This project provides dual execution frameworks: a lightweight, robust **Command Line Interface (CLI)** and a premium, highly interactive **Web Dashboard UI** built with Streamlit.

---

## 🌟 Key Features

* **Dual-Interface Control:** Run trades directly from the terminal or launch a responsive browser trading desk.
* **Bonus Objective Completed:** Native support for conditional `STOP_LIMIT` orders alongside standard `MARKET` and `LIMIT` strategies.
* **Resilient Architecture:** Features defensive programmatic **Clock Synchronization** to dynamically mitigate server-side clock drift errors (`API Error Code -1021`).
* **Production-Grade Logging:** Split-stream design. Human-centric status signals print to the console, while detailed JSON network traces log to `logs/trading_bot.log`.
* **Enterprise Security Guardrails:** Zero hardcoded credentials. Connects securely via local shell environment parameters.

---

## 📋 System Requirements

* **Language Environment:** Python 3.8 to 3.11+
* **Core Dependencies:** `python-binance`, `streamlit` (tracked within `requirements.txt`)
* **Credentials:** Free Binance Futures Demo Account API & Secret keys.

---

## 📂 Project Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py          # Network client initialization & time sync
│   ├── orders.py          # Execution match payload builders
│   ├── validators.py      # Pre-flight data-type validation logic
│   └── logging_config.py  # Log routing setup
│
├── logs/
│   └── trading_bot.log    # Compulsory transaction trace trails
│
├── app.py                 # Streamlit Interactive Web Interface Engine
├── cli.py                 # Structural CLI Gateway
├── requirements.txt       # Unified project dependency manifesto
└── README.md              # User instruction manual
