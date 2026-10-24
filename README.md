<<<<<<< HEAD
# NSE Live Market Analyzer & Prediction Dashboard

A fresh local Windows app for Indian NSE stocks. It provides live-ish quote refresh, technical analysis, candle charts, news headlines, and an experimental next-5-minute forecast.

## Data-source honesty
This app uses Yahoo Finance via yfinance for quotes/history and Yahoo RSS for headlines. These are unofficial sources; intraday data may be delayed, rate-limited, incomplete, or unavailable. It is not a guaranteed exchange-grade real-time feed. No paid API, AWS, or broker account is required. During market closure, last available data may be shown.

## Features
- Streamlit dashboard with auto-refresh
- NSE tickers (`RELIANCE.NS`, `TCS.NS`, `INFY.NS`, `HDFCBANK.NS`, `SBIN.NS`, `^NSEI` for Nifty 50)
- Price, change, volume, 1-minute / 5-minute / daily history
- RSI, MACD, EMA, SMA, Bollinger bands, ATR, returns and volatility
- Experimental Random Forest forecast for next 5-minute close and direction, only when sufficient intraday candles are available
- Latest related headlines via Yahoo Finance RSS
- Downloadable candle data and indicators
- Optional Docker setup not required for this dashboard-only version

## Run on Windows
Install Python 3.11 or newer. Extract the ZIP and open PowerShell in the extracted folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Open the local address Streamlit prints, usually `http://localhost:8501`.

If PowerShell blocks environment activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Ticker examples
- `RELIANCE.NS` Reliance Industries
- `TCS.NS` Tata Consultancy Services
- `INFY.NS` Infosys
- `HDFCBANK.NS` HDFC Bank
- `ICICIBANK.NS` ICICI Bank
- `SBIN.NS` State Bank of India
- `^NSEI` Nifty 50 index (history support may vary)

## Important
Predictions are uncertain statistical estimates, not financial advice or buy/sell instructions. Model probability is not calibrated confidence. Evaluate with a walk-forward backtest before considering any trading use. Do not use this app as a sole basis for financial decisions.
=======
# MARKET_DESK
>>>>>>> f7f2b8d68a1b0957e6be8ef45362b6089dc2c2df
