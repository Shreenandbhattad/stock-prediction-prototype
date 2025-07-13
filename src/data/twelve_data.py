"""
Module for fetching and processing data from the Twelve Data API.
"""
import requests
from typing import Any, Dict
from src.config import get_settings

# Get configuration
settings = get_settings()

def fetch_stock_data(symbol: str) -> Dict[str, Any]:
    """
    Fetch stock data including OHLCV and volume.
    """
    endpoint = f"{settings.twelve_data.base_url}/time_series"
    params = {
        "symbol": symbol,
        "interval": "1h",
        "apikey": settings.twelve_data.api_key
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()

def fetch_financial_statements(symbol: str) -> Dict[str, Any]:
    """
    Fetch financial statements like income statement, balance sheet, and cash flow.
    """
    endpoint = f"{settings.twelve_data.base_url}/financials"
    params = {
        "symbol": symbol,
        "apikey": settings.twelve_data.api_key
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()

def fetch_company_info(symbol: str) -> Dict[str, Any]:
    """
    Fetch company info like market cap, sector, and industry ratios.
    """
    endpoint = f"{settings.twelve_data.base_url}/company_info"
    params = {
        "symbol": symbol,
        "apikey": settings.twelve_data.api_key
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()

def fetch_economic_data() -> Dict[str, Any]:
    """
    Fetch economic data like interest rates, inflation, and GDP growth.
    """
    endpoint = f"{settings.twelve_data.base_url}/economic_data"
    params = {
        "apikey": settings.twelve_data.api_key
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()

def fetch_news_sentiment(symbol: str) -> Dict[str, Any]:
    """
    Fetch news sentiment and analysis for a specific company.
    """
    endpoint = f"{settings.twelve_data.base_url}/news_sentiment"
    params = {
        "symbol": symbol,
        "apikey": settings.twelve_data.api_key
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()
