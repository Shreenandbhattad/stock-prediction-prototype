"""
MarketStack API client for fetching stock data.
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from src.config import get_settings
import time

settings = get_settings()

class MarketStackClient:
    """Client for interacting with MarketStack API"""
    
    def __init__(self):
        self.api_key = settings.marketstack.api_key
        self.base_url = settings.marketstack.base_url
        self.session = requests.Session()
        
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to MarketStack API with error handling"""
        params['access_key'] = self.api_key
        
        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from MarketStack: {e}")
            return {}
    
    def get_stock_data(self, symbol: str, days: int = 365) -> pd.DataFrame:
        """
        Get historical stock data (OHLCV) for a symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            days: Number of days of historical data
            
        Returns:
            DataFrame with OHLCV data
        """
        date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        params = {
            'symbols': symbol,
            'date_from': date_from,
            'limit': 1000
        }
        
        data = self._make_request('eod', params)
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            df.set_index('date', inplace=True)
            return df[['open', 'high', 'low', 'close', 'volume']]
        
        return pd.DataFrame()
    
    def get_intraday_data(self, symbol: str, interval: str = '1min') -> pd.DataFrame:
        """
        Get intraday stock data
        
        Args:
            symbol: Stock symbol
            interval: Time interval (1min, 5min, 15min, 30min, 1hour)
            
        Returns:
            DataFrame with intraday data
        """
        params = {
            'symbols': symbol,
            'interval': interval,
            'limit': 1000
        }
        
        data = self._make_request('intraday', params)
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            df.set_index('date', inplace=True)
            return df[['open', 'high', 'low', 'close', 'volume']]
        
        return pd.DataFrame()
    
    def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get company information - Note: MarketStack doesn't provide this directly
        We'll create a mock implementation for now
        """
        # This is a mock implementation since MarketStack doesn't provide company info
        return {
            'symbol': symbol,
            'name': f"{symbol} Company",
            'sector': 'Technology',
            'industry': 'Software',
            'market_cap': 1000000000,  # Mock data
            'pe_ratio': 25.0,
            'dividend_yield': 0.02
        }
    
    def get_dividends(self, symbol: str) -> pd.DataFrame:
        """
        Get dividend data for a symbol
        
        Args:
            symbol: Stock symbol
            
        Returns:
            DataFrame with dividend data
        """
        params = {
            'symbols': symbol,
            'limit': 100
        }
        
        data = self._make_request('dividends', params)
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        
        return pd.DataFrame()
    
    def get_splits(self, symbol: str) -> pd.DataFrame:
        """
        Get stock split data
        
        Args:
            symbol: Stock symbol
            
        Returns:
            DataFrame with split data
        """
        params = {
            'symbols': symbol,
            'limit': 100
        }
        
        data = self._make_request('splits', params)
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        
        return pd.DataFrame()

# Global client instance
marketstack_client = MarketStackClient()
