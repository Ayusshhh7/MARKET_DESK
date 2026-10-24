
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import numpy as np
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="Market Desk",
    page_icon="📈",
    layout="wide"
)

# ---------- THEME TOGGLE ----------
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

st.sidebar.markdown("### 🎨 Appearance")

st.sidebar.toggle(
    "Light theme",
    key="light_theme",
    value=(st.session_state.theme == "Light")
)

st.session_state.theme = (
    "Light" if st.session_state.light_theme else "Dark"
)

is_light = st.session_state.theme == "Light"

if is_light:
    BG = "#f4f7fb"
    PANEL = "#ffffff"
    TEXT = "#172033"
    MUTED = "#64748b"
    GRID = "#e2e8f0"
    GREEN = "#059669"
    RED = "#e54861"
    BLUE = "#2563eb"
    PURPLE = "#7c3aed"
else:
    BG = "#0b1017"
    PANEL = "#111923"
    TEXT = "#edf3f8"
    MUTED = "#93a4b7"
    GRID = "#243141"
    GREEN = "#20c997"
    RED = "#ff647c"
    BLUE = "#64a8ff"
    PURPLE = "#c49bff"


from pathlib import Path
import streamlit as st

css_path = Path(__file__).parent / "market.css"
css = css_path.read_text(encoding="utf-8")

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Make the external stylesheet follow your theme toggle
st.markdown(f"""
<style>
:root {{
    --md-bg: {BG};
    --md-panel: {PANEL};
    --md-text: {TEXT};
    --md-muted: {MUTED};
    --md-line: {GRID};
    --md-green: {GREEN};
}}
</style>
""", unsafe_allow_html=True)

# ---------- PREMIUM DARK UI ----------


st.markdown(f"""
<style>

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

[data-testid="stHeader"] {{
    background-color: {BG};
}}

[data-testid="stSidebar"] {{
    background-color: {PANEL};
    border-right: 1px solid {GRID};
}}

[data-testid="stSidebar"] * {{
    color: {TEXT};
}}

[data-testid="stSidebar"] input {{
    background-color: {PANEL};
    color: {TEXT};
}}

[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: {PANEL};
    border-color: {GRID};
    color: {TEXT};
}}

[data-testid="stSidebar"] div[data-baseweb="select"] * {{
    color: {TEXT};
}}

[data-testid="stMetric"] {{
    background-color: {PANEL};
    border: 1px solid {GRID};
    border-radius: 14px;
    padding: 16px;
}}

[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
}}

[data-testid="stMetricValue"] {{
    color: {TEXT} !important;
}}

h1, h2, h3, p, label {{
    color: {TEXT};
}}

[data-testid="stCaptionContainer"] {{
    color: {MUTED};
}}

div[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {GREEN} !important;
    border-bottom-color: {GREEN} !important;
}}

div[data-baseweb="popover"],
div[data-baseweb="menu"] {{
    background-color: {PANEL};
}}

div[data-baseweb="popover"] * {{
    color: {TEXT};
}}

hr {{
    border-color: {GRID};
}}
 [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: #ffffff !important;
    border: 1px solid #d5deea !important;
}}

[data-testid="stSidebar"] div[data-baseweb="select"] span,
[data-testid="stSidebar"] div[data-baseweb="select"] input {{
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}}

[data-testid="stSidebar"] input::placeholder {{
    color: #7b8798 !important;
    -webkit-text-fill-color: #7b8798 !important;
    opacity: 1 !important;
}}

[data-testid="stSidebar"] div[data-baseweb="select"] svg {{
    fill: #172033 !important;
    color: #172033 !important;
}}

[data-testid="stRadio"] label {{
    color: #172033 !important;
}}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {{
    color: #172033 !important;
    fill: #172033 !important;
}}

[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: #ffffff !important;
    border-color: #d5deea !important;
}}
</style>
""", unsafe_allow_html=True)



# ---------- SIDEBAR ----------
st.sidebar.title("◈ MARKET DESK")

# Popular stocks and market assets
assets = {
    "🇮🇳 Indian Stocks": {
        "Reliance Industries": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "State Bank of India": "SBIN.NS",
        "ITC": "ITC.NS",
        "Bharti Airtel": "BHARTIARTL.NS",
        "Tata Motors": "TMPV.NS",
        "Larsen & Toubro": "LT.NS",
        "Bajaj Finance": "BAJFINANCE.NS",
        "Wipro": "WIPRO.NS",
        "Adani Enterprises": "ADANIENT.NS",
        "Maruti Suzuki": "MARUTI.NS",
        "Axis Bank": "AXISBANK.NS",
    },
    "🇺🇸 US Stocks": {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Amazon": "AMZN",
        "Alphabet (Google)": "GOOGL",
        "Meta": "META",
        "Tesla": "TSLA",
        "AMD": "AMD",
        "Netflix": "NFLX",
        "Walmart": "WMT",
        "Berkshire Hathaway": "BRK-B",
    },
    "💱 Currencies": {
        "US Dollar / Indian Rupee": "USDINR=X",
        "Euro / US Dollar": "EURUSD=X",
        "British Pound / US Dollar": "GBPUSD=X",
        "US Dollar / Japanese Yen": "JPY=X",
    },
    "🥇 Precious Metals": {
        "Gold (USD per ounce)": "GC=F",
        "Silver (USD per ounce)": "SI=F",
        "Gold ETF (GLD)": "GLD",
        "Silver ETF (SLV)": "SLV",
    },
    "📊 Market Indices": {
        "Nifty 50": "^NSEI",
        "BSE Sensex": "^BSESN",
        "S&P 500": "^GSPC",
        "NASDAQ Composite": "^IXIC",
        "Dow Jones": "^DJI",
    },
}

st.sidebar.markdown("### 📈 Choose an Asset")

category = st.sidebar.selectbox(
    "Market category",
    list(assets.keys()),
    index=0,
)

selected_name = st.sidebar.selectbox(
    "Popular companies and assets",
    list(assets[category].keys()),
    index=0,
)

selected_ticker = assets[category][selected_name]

custom_ticker = st.sidebar.text_input(
    "Or enter a custom ticker",
    value="",
    placeholder="e.g. ZOMATO.NS or MSFT",
).strip().upper()

ticker = custom_ticker if custom_ticker else selected_ticker

st.sidebar.caption(f"Selected symbol: `{ticker}`")

timeframe = st.sidebar.selectbox(
    "Chart timeframe",
    ["1 minute", "5 minutes", "15 minutes", "1 day"]
)

period = st.sidebar.selectbox(
    "History",
    ["1 day", "5 days", "1 month", "3 months"]
)

auto_refresh = st.sidebar.checkbox(
    "Auto refresh every 60 seconds",
    value=True
)
if auto_refresh:
    st.markdown(
        '<meta http-equiv="refresh" content="60">',
        unsafe_allow_html=True
    )

intervals = {
    "1 minute": "1m",
    "5 minutes": "5m",
    "15 minutes": "15m",
    "1 day": "1d"
}

periods = {
    "1 day": "1d",
    "5 days": "5d",
    "1 month": "1mo",
    "3 months": "3mo"
}

# ---------- FETCH MARKET DATA ----------
@st.cache_data(ttl=45)
def get_data(symbol, selected_period, selected_interval):
    return yf.Ticker(symbol).history(
        period=selected_period,
        interval=selected_interval,
        auto_adjust=False
    )


st.markdown("""
<div class="md-app-header">
    <div class="md-brand">
        <div class="md-logo">↗</div>
        <div>
            <div class="md-app-name">Market Desk</div>
            <div class="md-app-subtitle">
                Smart market analytics · Technical indicators · Price insights
            </div>
        </div>
    </div>
    <div class="md-live-pill">
        <span class="md-live-dot"></span>
        MARKET DATA
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 📈 Market Overview")

st.caption("Market Intelligence · Technical Analysis")

try:
    with st.spinner("Loading market data..."):
        data = get_data(
            ticker,
            periods[period],
            intervals[timeframe]
        )

    if data.empty:
        st.error(
            "No data available. Check the symbol or try again later."
        )
        st.stop()

except Exception as error:
    st.error(f"Could not fetch market data: {error}")
    st.stop()


# ---------- CLEAN MARKET DATA ----------
data = data.dropna(
    subset=["Open", "High", "Low", "Close"]
).sort_index()

data = data[~data.index.duplicated(keep="last")]
# Convert chart timestamps to Indian Standard Time
if data.index.tz is not None:
    data.index = data.index.tz_convert(
        ZoneInfo("Asia/Kolkata")
    )

# ---------- INDICATORS ----------
close = data["Close"]

data["EMA9"] = close.ewm(span=9, adjust=False).mean()
data["EMA21"] = close.ewm(span=21, adjust=False).mean()
data["SMA20"] = close.rolling(20).mean()

delta = close.diff()
gain = delta.clip(lower=0).ewm(
    alpha=1/14, adjust=False
).mean()

loss = (-delta.clip(upper=0)).ewm(
    alpha=1/14, adjust=False
).mean()

rs = gain / loss.replace(0, np.nan)
data["RSI"] = 100 - (100 / (1 + rs))

ema12 = close.ewm(span=12, adjust=False).mean()
ema26 = close.ewm(span=26, adjust=False).mean()

data["MACD"] = ema12 - ema26
data["SIGNAL"] = data["MACD"].ewm(
    span=9, adjust=False
).mean()

data["BB_MID"] = close.rolling(20).mean()
std = close.rolling(20).std()

data["BB_UPPER"] = data["BB_MID"] + 2 * std
data["BB_LOWER"] = data["BB_MID"] - 2 * std

last = data.iloc[-1]
previous = data.iloc[-2] if len(data) > 1 else last

price = float(last["Close"])
change = price - float(previous["Close"])
change_pct = (
    change / float(previous["Close"]) * 100
    if previous["Close"] else 0
)

currency = "" if ticker.startswith("^") else "₹"

# ---------- TOP METRICS ----------
a, b, c, d = st.columns(4)

a.metric(
    "Latest Available Price",
    f"{currency}{price:,.2f}",
    f"{change:+.2f} ({change_pct:+.2f}%)"
)

b.metric(
    "RSI (14)",
    f"{last['RSI']:.1f}"
    if pd.notna(last["RSI"]) else "—"
)

c.metric(
    "EMA 9",
    f"{currency}{last['EMA9']:,.2f}"
)

d.metric(
    "Volume",
    f"{float(last['Volume']):,.0f}"
)

st.divider()

# ---------- MAIN PRICE CHART ----------
st.subheader("Price Action")

chart_type = st.radio(
    "Chart style",
    ["Candlestick", "Line", "Area"],
    horizontal=True
)
chart_x = data.index.strftime("%H:%M")
fig = go.Figure()

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=chart_x,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Price",
        increasing_line_color="#20c997",
        decreasing_line_color="#ff647c",
        increasing_fillcolor="#20c997",
        decreasing_fillcolor="#ff647c"
    ))

elif chart_type == "Line":
    fig.add_trace(go.Scatter(
        x=chart_x,
        y=data["Close"],
        mode="lines",
        name="Price",
        line=dict(color="#20c997", width=2.5)
    ))

else:
    fig.add_trace(go.Scatter(
        x=chart_x,
        y=data["Close"],
        mode="lines",
        name="Price",
        line=dict(color="#20c997", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(32,201,151,0.10)"
    ))

# Moving averages
fig.add_trace(go.Scatter(
    x=chart_x,
    y=data["EMA9"],
    name="EMA 9",
    line=dict(color="#64a8ff", width=1.5)
))

fig.add_trace(go.Scatter(
    x=chart_x,
    y=data["EMA21"],
    name="EMA 21",
    line=dict(color="#c49bff", width=1.5)
))

fig.update_layout(
    template="plotly_white" if is_light else "plotly_dark",
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    font=dict(
    family="Arial, sans-serif",
    size=12,
    color=TEXT
   ),
    height=440,
    margin=dict(l=10, r=10, t=30, b=10),
    hovermode="x unified",
    dragmode="pan",

   

xaxis=dict(
    type="category",
    showgrid=False,
    tickangle=0,
    nticks=6,
    tickformat="%H:%M",
    tickfont=dict(color=TEXT, size=10),
    rangeslider=dict(visible=False),
    showspikes=True,
    spikemode="across",
    spikesnap="cursor"
),


   yaxis=dict(
    side="right",
    showgrid=True,
    gridcolor=GRID,
    tickfont=dict(color=TEXT, size=10),
    autorange=True,
    automargin=True
),
    legend=dict(
    orientation="h",
    y=1.04,
    x=0,
    font=dict(color=TEXT, size=11)
    ),
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displaylogo": False,
        "scrollZoom": True
    }
)

# ---------- TECHNICAL ANALYSIS ----------
left, right = st.columns(2)

with left:
    st.subheader("RSI Momentum")

    rsi_fig = go.Figure()

    rsi_fig.add_trace(go.Scatter(
        x=chart_x,
        y=data["RSI"],
        name="RSI",
        line=dict(color="#c49bff", width=2)
    ))

    rsi_fig.add_hline(
        y=70,
        line_dash="dot",
        line_color="#ff647c"
    )

    rsi_fig.add_hline(
        y=30,
        line_dash="dot",
        line_color="#20c997"
    )

    

    rsi_fig.update_layout(
        template="plotly_white" if is_light else "plotly_dark",
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color=TEXT, size=11),
        height=300,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(
            showgrid=False,
            tickangle=0,
            nticks=6,
            tickfont=dict(color=TEXT, size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID,
            tickfont=dict(color=TEXT, size=10),
            range=[0, 100]
        )
    )



    st.plotly_chart(rsi_fig, use_container_width=True)

with right:
    st.subheader("MACD Trend")

    macd_fig = go.Figure()

    macd_fig.add_trace(go.Scatter(
        x=chart_x,
        y=data["MACD"],
        name="MACD",
        line=dict(color="#64a8ff", width=2)
    ))

    macd_fig.add_trace(go.Scatter(
        x=chart_x,
        y=data["SIGNAL"],
        name="Signal",
        line=dict(color="#ffbf69", width=1.5)
    ))

    
    macd_fig.update_layout(
    template="plotly_white" if is_light else "plotly_dark",
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    font=dict(color=TEXT, size=11),
    height=300,
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(
        showgrid=False,
        tickangle=0,
        nticks=6,
        tickfont=dict(color=TEXT, size=10)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor=GRID,
        tickfont=dict(color=TEXT, size=10)
    ),
    legend=dict(
        orientation="h",
        y=1.05,
        x=0,
        font=dict(color=TEXT, size=10)
    )
)


    st.plotly_chart(macd_fig, use_container_width=True)

# ---------- TREND SUMMARY ----------
st.subheader("Technical Snapshot")

trend = (
    "Bullish bias"
    if last["EMA9"] > last["EMA21"]
    else "Bearish bias"
)

st.write(f"**EMA trend:** {trend}")

if pd.notna(last["RSI"]):
    if last["RSI"] >= 70:
        st.write("RSI is elevated (70+).")
    elif last["RSI"] <= 30:
        st.write("RSI is low (30 or below).")
    else:
        st.write("RSI is between 30 and 70.")

st.caption(
    "Data source: Yahoo Finance (unofficial). "
    "Data may be delayed or unavailable. "
    "Indicators are educational and are not financial advice."
)

# ---------- DOWNLOAD DATA ----------
st.subheader("Historical Data")

st.download_button(
    "Download data as CSV",
    data=data.to_csv().encode("utf-8"),
    file_name=f"{ticker.replace('^', '')}_analysis.csv",
    mime="text/csv"
)

st.dataframe(
    data.sort_index(ascending=False).head(30),
    use_container_width=True
)
