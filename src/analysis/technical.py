"""
Module for calculating technical indicators for the stock prediction prototype.
"""
import pandas as pd
import numpy as np
try:
    import talib
except ImportError:
    print("Warning: TA-Lib not installed. Using pandas-ta instead.")
    import pandas_ta as ta


def calculate_moving_averages(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate various moving averages for the stock data.
    """
    data['SMA'] = talib.SMA(data['close'], timeperiod=30)
    data['EMA'] = talib.EMA(data['close'], timeperiod=30)
    data['WMA'] = talib.WMA(data['close'], timeperiod=30)
    return data


def calculate_macd(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate MACD for the stock data.
    """
    data['MACD'], data['MACDSignal'], data['MACDHist'] = talib.MACD(data['close'],
                                                                    fastperiod=12, slowperiod=26, signalperiod=9)
    return data


def calculate_rsi(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate RSI for the stock data.
    """
    data['RSI'] = talib.RSI(data['close'], timeperiod=14)
    return data


def calculate_adx(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate ADX for the stock data.
    """
    data['ADX'] = talib.ADX(data['high'], data['low'], data['close'], timeperiod=14)
    return data


def calculate_bollinger_bands(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Bollinger Bands for the stock data.
    """
    data['UpperBand'], data['MiddleBand'], data['LowerBand'] = talib.BBANDS(data['close'],
                                                                             timeperiod=20,
                                                                             nbdevup=2,
                                                                             nbdevdn=2,
                                                                             matype=0)
    return data

# Add more technical indicator calculations as needed.
