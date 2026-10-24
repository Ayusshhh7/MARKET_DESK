# Market Desk — Live Stock Market Analyzer

A local Windows dashboard for tracking stocks, analyzing price movements, viewing technical indicators, and experimenting with short-term price forecasts.

## Features

- Interactive candlestick, line, and area charts
- Moving averages: EMA 9, EMA 21, and SMA 20
- Technical indicators: RSI and MACD
- Selectable stocks, currencies, precious metals, and market indices
- Configurable chart intervals and historical windows
- Light and dark themes
- Manual market-data refresh
- CSV export of historical data
- Experimental short-term price forecasting, if enabled in the application

## Data Source

The application uses Yahoo Finance through `yfinance` for market quotes and historical data.

Data availability, update frequency, and intraday intervals depend on the selected asset and the data provider. Prices may be delayed, incomplete, or unavailable. This is not a guaranteed real-time trading feed.

## Requirements

- Python 3.11 or compatible version
- Packages listed in `requirements.txt`

## Run Locally

Create and activate a virtual environment if you do not already have one.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed in your terminal.

## Project Files

- `app.py` — application and dashboard logic
- `market.css` — custom styling
- `requirements.txt` — Python dependencies
- `README.md` — project documentation

## Disclaimer

This project is for educational and informational purposes only. Its indicators and experimental forecasts are not financial advice and should not be used as the sole basis for investment decisions.