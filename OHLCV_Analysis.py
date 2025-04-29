import pandas as pd
import yfinance as yf
import datetime as dt
import numpy as np

tickers = ["YPFD.BA","AAPL","ALUA.BA"]

start = dt.datetime.today() - dt.timedelta(30)
end = dt.datetime.today()

def ema(series, length):
    return series.ewm(span=length, adjust=False).mean()

def rsi(data, n):
    "Función para calcular el RSI"
    df = data.copy()
    
    # Calcular la diferencia de precios (cambio)
    change = df["Close"].diff()

    # Calcular ganancias y pérdidas
    df["gain"] = np.where(change > 0, change, 0)
    df["loss"] = np.where(change < 0, -change, 0)

    # Calcular las medias exponenciales de ganancias y pérdidas
    avgGain = df["gain"].ewm(span=n, min_periods=n).mean()
    avgLoss = df["loss"].ewm(span=n, min_periods=n).mean()

    # Evitar división por cero en RS
    rs = avgGain / avgLoss.replace(0, np.nan)

    # Calcular RSI
    df["RSI"] = 100 - (100 / (1 + rs))
    return df["RSI"]

for ticker in tickers:
    yfinance_information = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=False)

    data = pd.DataFrame(yfinance_information)

    data.columns = ["Adj Close",'Close', 'High', 'Low', 'Open', 'Vol']
    data['Ticker'] = ticker
    data["date"] = data.index

    data.info()
    data["EMA"] = ema(data["Close"], 50)
    data["RSI"] = rsi(data, 14)

    print(data)

daily_data = data.resample('D').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Vol': 'sum',
    'Adj Close': 'last'
})


# Supongamos una serie con índice datetime
rng = pd.date_range(start, periods=5, freq="D")
ts = pd.Series(range(5), index=rng)

# Convertimos de timestamp a period mensual
ts_period = ts.to_period("M")
print(ts_period)


# Crear intervalos de 2 días a partir de fechas
intervals = pd.interval_range(start=start, end=end, freq="2D")

# Crear un DataFrame con fechas
dates = pd.date_range(start, periods=10, freq="D")
df = pd.DataFrame({"value": range(10)}, index=dates)

# Asignar intervalos según la fecha
df["interval"] = pd.cut(df.index, bins=intervals)
print(df.head())

# Simulación de tiempo relativo: segundos desde el inicio
elapsed_time = np.arange(0, 10, 0.5)  # cada 0.5 segundos
sensor_data = pd.Series(np.random.randn(len(elapsed_time)), index=elapsed_time)
sensor_data.index.name = "segundos_desde_inicio"

print(sensor_data.head())
