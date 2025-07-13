"""
Comprehensive technical analysis module with pandas-based calculations.
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple

class TechnicalIndicators:
    """Class for calculating technical indicators using pandas"""
    
    @staticmethod
    def sma(data: pd.Series, window: int = 20) -> pd.Series:
        """Simple Moving Average"""
        return data.rolling(window=window).mean()
    
    @staticmethod
    def ema(data: pd.Series, window: int = 20) -> pd.Series:
        """Exponential Moving Average"""
        return data.ewm(span=window).mean()
    
    @staticmethod
    def wma(data: pd.Series, window: int = 20) -> pd.Series:
        """Weighted Moving Average"""
        weights = np.arange(1, window + 1)
        return data.rolling(window=window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
    
    @staticmethod
    def rsi(data: pd.Series, window: int = 14) -> pd.Series:
        """Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """MACD (Moving Average Convergence Divergence)"""
        ema_fast = TechnicalIndicators.ema(data, fast)
        ema_slow = TechnicalIndicators.ema(data, slow)
        macd_line = ema_fast - ema_slow
        signal_line = TechnicalIndicators.ema(macd_line, signal)
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    @staticmethod
    def bollinger_bands(data: pd.Series, window: int = 20, num_std: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Bollinger Bands"""
        sma = TechnicalIndicators.sma(data, window)
        std = data.rolling(window=window).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return upper_band, sma, lower_band
    
    @staticmethod
    def stochastic_oscillator(high: pd.Series, low: pd.Series, close: pd.Series, k_window: int = 14, d_window: int = 3) -> Tuple[pd.Series, pd.Series]:
        """Stochastic Oscillator"""
        lowest_low = low.rolling(window=k_window).min()
        highest_high = high.rolling(window=k_window).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_window).mean()
        return k_percent, d_percent
    
    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
        """Average True Range"""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return true_range.rolling(window=window).mean()
    
    @staticmethod
    def adx(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
        """Average Directional Index (simplified version)"""
        plus_dm = high.diff()
        minus_dm = -low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        tr = TechnicalIndicators.atr(high, low, close, window)
        plus_di = 100 * (plus_dm.rolling(window=window).mean() / tr)
        minus_di = 100 * (minus_dm.rolling(window=window).mean() / tr)
        
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        return dx.rolling(window=window).mean()
    
    @staticmethod
    def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        """On-Balance Volume"""
        obv = pd.Series(index=close.index, dtype=float)
        obv.iloc[0] = volume.iloc[0]
        
        for i in range(1, len(close)):
            if close.iloc[i] > close.iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] + volume.iloc[i]
            elif close.iloc[i] < close.iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] - volume.iloc[i]
            else:
                obv.iloc[i] = obv.iloc[i-1]
        
        return obv
    
    @staticmethod
    def vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
        """Volume Weighted Average Price"""
        typical_price = (high + low + close) / 3
        return (typical_price * volume).cumsum() / volume.cumsum()
    
    @staticmethod
    def williams_r(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
        """Williams %R"""
        highest_high = high.rolling(window=window).max()
        lowest_low = low.rolling(window=window).min()
        return -100 * ((highest_high - close) / (highest_high - lowest_low))

def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all technical indicators for a given DataFrame
    
    Args:
        df: DataFrame with columns ['open', 'high', 'low', 'close', 'volume']
        
    Returns:
        DataFrame with all technical indicators added
    """
    # Ensure we have the required columns
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"DataFrame must contain columns: {required_columns}")
    
    # Create a copy to avoid modifying original
    result = df.copy()
    
    # Moving averages
    result['SMA_20'] = TechnicalIndicators.sma(df['close'], 20)
    result['SMA_50'] = TechnicalIndicators.sma(df['close'], 50)
    result['EMA_12'] = TechnicalIndicators.ema(df['close'], 12)
    result['EMA_26'] = TechnicalIndicators.ema(df['close'], 26)
    result['WMA_20'] = TechnicalIndicators.wma(df['close'], 20)
    
    # RSI
    result['RSI'] = TechnicalIndicators.rsi(df['close'])
    
    # MACD
    macd_line, signal_line, histogram = TechnicalIndicators.macd(df['close'])
    result['MACD'] = macd_line
    result['MACD_Signal'] = signal_line
    result['MACD_Histogram'] = histogram
    
    # Bollinger Bands
    bb_upper, bb_middle, bb_lower = TechnicalIndicators.bollinger_bands(df['close'])
    result['BB_Upper'] = bb_upper
    result['BB_Middle'] = bb_middle
    result['BB_Lower'] = bb_lower
    
    # Stochastic Oscillator
    stoch_k, stoch_d = TechnicalIndicators.stochastic_oscillator(df['high'], df['low'], df['close'])
    result['Stoch_K'] = stoch_k
    result['Stoch_D'] = stoch_d
    
    # ATR
    result['ATR'] = TechnicalIndicators.atr(df['high'], df['low'], df['close'])
    
    # ADX
    result['ADX'] = TechnicalIndicators.adx(df['high'], df['low'], df['close'])
    
    # OBV
    result['OBV'] = TechnicalIndicators.obv(df['close'], df['volume'])
    
    # VWAP
    result['VWAP'] = TechnicalIndicators.vwap(df['high'], df['low'], df['close'], df['volume'])
    
    # Williams %R
    result['Williams_R'] = TechnicalIndicators.williams_r(df['high'], df['low'], df['close'])
    
    return result

def get_technical_summary(df: pd.DataFrame) -> Dict:
    """
    Get a technical analysis summary for the latest data point
    
    Args:
        df: DataFrame with technical indicators
        
    Returns:
        Dictionary with technical analysis summary
    """
    if df.empty:
        return {}
    
    latest = df.iloc[-1]
    
    # Trend indicators
    trend_score = 0
    if latest['close'] > latest['SMA_20']:
        trend_score += 1
    if latest['close'] > latest['SMA_50']:
        trend_score += 1
    if latest['EMA_12'] > latest['EMA_26']:
        trend_score += 1
    
    # Momentum indicators
    momentum_score = 0
    if latest['RSI'] > 50:
        momentum_score += 1
    if latest['MACD'] > latest['MACD_Signal']:
        momentum_score += 1
    if latest['Stoch_K'] > latest['Stoch_D']:
        momentum_score += 1
    
    # Generate signals
    signals = []
    if latest['RSI'] > 70:
        signals.append("RSI Overbought")
    elif latest['RSI'] < 30:
        signals.append("RSI Oversold")
    
    if latest['close'] > latest['BB_Upper']:
        signals.append("Above Bollinger Upper Band")
    elif latest['close'] < latest['BB_Lower']:
        signals.append("Below Bollinger Lower Band")
    
    return {
        'trend_score': trend_score,
        'momentum_score': momentum_score,
        'signals': signals,
        'rsi': latest['RSI'],
        'macd': latest['MACD'],
        'sma_20': latest['SMA_20'],
        'sma_50': latest['SMA_50'],
        'current_price': latest['close']
    }
