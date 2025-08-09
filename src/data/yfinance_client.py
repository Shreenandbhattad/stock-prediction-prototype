import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(symbol: str, days: int = 2000) -> pd.DataFrame:
    """
    Gets historical stock data from Yahoo Finance.
    """
    stock = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    df = stock.history(start=start_date, end=end_date)

    if df.empty:
        return pd.DataFrame()

    # Rename columns to be consistent with the rest of the application
    df.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    }, inplace=True)

    # Ensure index is datetime and timezone-naive for consistency
    df.index = pd.to_datetime(df.index).tz_localize(None)

    return df[['open', 'high', 'low', 'close', 'volume']]
