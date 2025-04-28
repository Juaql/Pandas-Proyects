import pandas as pd
import yfinance as yf
import datetime as dt

tickers = ["YPFD.BA","AAPL","ALUA.BA"]

start = dt.datetime.today() - dt.timedelta(7)
end = dt.datetime.today()

for ticker in tickers:
    yfinance_information = yf.download(ticker, start=start, end=end, interval="15m", auto_adjust=False)

    data = pd.DataFrame(yfinance_information)

    data.columns = ["Adj Close",'Close', 'High', 'Low', 'Open', 'Vol']
    data['Ticker'] = ticker
    data["date"] = data.index

    data.info()

