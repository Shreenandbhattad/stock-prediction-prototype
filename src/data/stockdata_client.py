import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any

class StockDataClient:
    """Client for interacting with the stockdata.org API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stockdata.org/v1"
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the API with error handling"""
        params['api_token'] = self.api_key
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from StockData.org: {e}")
            return {}

    def get_stock_data(self, symbol: str, days: int = 1000) -> pd.DataFrame:
        """Get historical EOD stock data (OHLCV) for a symbol."""
        params = {
            'symbols': symbol,
            'limit': days,
            'sort': 'desc' # Get the most recent data
        }
        data = self._make_request('/data/eod', params)

        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df.sort_index(inplace=True) # Sort ascending by date
            return df[['open', 'high', 'low', 'close', 'volume']]

        return pd.DataFrame()

    def get_sentiment_data(self, symbol: str, days: int = 1000) -> pd.DataFrame:
        """Get historical daily sentiment data for a symbol."""
        date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        params = {
            'symbols': symbol,
            'interval': 'day',
            'published_after': date_from
        }
        data = self._make_request('/news/stats/intraday', params)

        if 'data' in data and data['data']:
            records = []
            for daily_data in data['data']:
                date = daily_data['date']
                for entity_data in daily_data['data']:
                    if entity_data['key'].upper() == symbol.upper():
                        records.append({
                            'date': date,
                            'sentiment_avg': entity_data['sentiment_avg']
                        })

            if not records:
                return pd.DataFrame()

            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df.sort_index(inplace=True)
            return df

        return pd.DataFrame()

from src.config import get_settings

# Get settings
settings = get_settings()

# Global client instance
stockdata_client = StockDataClient(api_key=settings.stockdata.api_key)
