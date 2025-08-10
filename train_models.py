import argparse
import pandas as pd
from src.data.stockdata_client import stockdata_client
from src.data.yfinance_client import get_stock_data as get_yfinance_data
from src.analysis.technical_indicators import calculate_all_indicators
from src.analysis.fundamental import get_historical_fundamental_data
from src.prediction.ml_models import StockPredictor

def train_for_symbol(symbol: str):
    """
    Fetches all data, trains all models, and saves the predictor to a file.
    """
    print(f"--- Starting training process for symbol: {symbol} ---")

    try:
        # 1. Fetch Price Data
        print("\n1. Fetching Price Data...")
        price_data = get_yfinance_data(symbol, days=2000) # Fetch more data for better training
        if price_data.empty:
            print(f"Error: Price data not found for {symbol}.")
            return
        print(f"Successfully fetched {len(price_data)} price data points.")

        # 2. Calculate Technical Indicators
        print("\n2. Calculating Technical Indicators...")
        indicators = calculate_all_indicators(price_data)
        print("Successfully calculated technical indicators.")

        # 3. Fetch Fundamental Data
        print("\n3. Fetching Fundamental Data...")
        fundamental_data = get_historical_fundamental_data(symbol)
        if fundamental_data.empty:
            print("Warning: Fundamental data not found.")
        else:
            print(f"Successfully fetched {len(fundamental_data)} fundamental records.")

        # 4. Fetch Sentiment Data (optional, will be handled gracefully if it fails)
        print("\n4. Fetching Sentiment Data...")
        sentiment_data = stockdata_client.get_sentiment_data(symbol, days=2000)
        if sentiment_data.empty:
            print("Warning: Sentiment data not found. This may be a premium feature.")
        else:
            print(f"Successfully fetched {len(sentiment_data)} sentiment records.")

        # 5. Merge All Data Sources
        print("\n5. Merging all data sources...")
        combined_data = indicators
        if not fundamental_data.empty:
            combined_data.index = pd.to_datetime(combined_data.index).tz_localize(None)
            fundamental_data.index = pd.to_datetime(fundamental_data.index).tz_localize(None)
            combined_data = pd.merge_asof(combined_data.sort_index(), fundamental_data.sort_index(), left_index=True, right_index=True, direction='backward')

        if not sentiment_data.empty:
            sentiment_data.index = pd.to_datetime(combined_data.index).tz_localize(None)
            sentiment_data.index = pd.to_datetime(sentiment_data.index).tz_localize(None)
            combined_data = pd.merge_asof(combined_data.sort_index(), sentiment_data.sort_index(), left_index=True, right_index=True, direction='backward')

        combined_data.fillna(method='ffill', inplace=True)
        # Drop any remaining NaNs from the start of the series
        combined_data.dropna(inplace=True)
        print("Successfully merged all data.")

        # 6. Train Models
        print("\n6. Training models (this will take a long time)...")
        predictor = StockPredictor()

        print("   - Preparing features...")
        X, y = predictor.prepare_features(combined_data)

        if len(X) < 100:
            print(f"Error: Not enough data ({len(X)} points) to train models for {symbol}.")
            return

        print("   - Training models with hyperparameter tuning...")
        training_results = predictor.train_models(X, y)
        print("Model training complete.")
        print("Training Results:", training_results)

        # 7. Save the trained predictor
        print("\n7. Saving trained model...")
        model_filepath = f"trained_models/{symbol.upper()}.pkl"
        predictor.save(model_filepath, training_results)

        print(f"\n--- Successfully trained and saved model for {symbol} to {model_filepath} ---")

    except Exception as e:
        print(f"\n--- An error occurred during training for {symbol} ---")
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train stock prediction models for a given symbol.")
    parser.add_argument("symbol", type=str, help="The stock symbol to train (e.g., AAPL, TSLA).")
    args = parser.parse_args()

    train_for_symbol(args.symbol)
