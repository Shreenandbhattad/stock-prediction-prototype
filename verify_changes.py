import pandas as pd
from src.data.stockdata_client import stockdata_client
from src.analysis.technical_indicators import calculate_all_indicators
from src.analysis.fundamental import get_historical_fundamental_data
from src.prediction.ml_models import StockPredictor, create_ensemble_prediction, generate_recommendation

def run_verification_test(symbol: str = "AAPL"):
    """
    Runs an end-to-end test of the new prediction pipeline with all data sources.
    """
    print(f"--- Starting New Pipeline Verification for symbol: {symbol} ---")

    try:
        # 1. Fetch Price Data
        print("\n1. Fetching Price Data from StockData.org...")
        price_data = stockdata_client.get_stock_data(symbol, days=1000)
        if price_data.empty:
            print("Error: Price data not found.")
            return
        print(f"Successfully fetched {len(price_data)} price data points.")

        # 2. Calculate Technical Indicators
        print("\n2. Calculating Technical Indicators...")
        indicators = calculate_all_indicators(price_data)
        print("Successfully calculated technical indicators.")

        # 3. Fetch Fundamental Data
        print("\n3. Fetching Fundamental Data from yfinance...")
        fundamental_data = get_historical_fundamental_data(symbol)
        if fundamental_data.empty:
            print("Warning: Fundamental data not found.")
        else:
            print(f"Successfully fetched {len(fundamental_data)} fundamental records.")

        # 4. Fetch Sentiment Data
        print("\n4. Fetching Sentiment Data from StockData.org...")
        sentiment_data = stockdata_client.get_sentiment_data(symbol, days=1000)
        if sentiment_data.empty:
            print("Warning: Sentiment data not found.")
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
            sentiment_data.index = pd.to_datetime(sentiment_data.index).tz_localize(None)
            combined_data = pd.merge_asof(combined_data.sort_index(), sentiment_data.sort_index(), left_index=True, right_index=True, direction='backward')

        combined_data.fillna(method='ffill', inplace=True)
        print("Successfully merged all data.")

        # 6. Run Prediction Pipeline
        print("\n6. Running prediction pipeline (this may take a while)...")
        predictor = StockPredictor()

        print("   - Preparing features...")
        X, y = predictor.prepare_features(combined_data)

        print("   - Training models with hyperparameter tuning...")
        training_results = predictor.train_models(X, y)

        print("   - Predicting future prices...")
        future_predictions = predictor.predict_future(combined_data, days=30)

        print("   - Creating weighted ensemble prediction...")
        ensemble_result = create_ensemble_prediction(future_predictions, training_results)

        current_price = price_data.iloc[-1]['close']
        recommendation = generate_recommendation(
            current_price,
            ensemble_result.get('ensemble_prediction', current_price),
            ensemble_result.get('confidence', 0.5)
        )
        print("Successfully completed prediction pipeline.")

        # 7. Print results
        print("\n--- Verification Results ---")
        print(f"Current Price: {current_price}")
        print(f"Ensemble Prediction: {ensemble_result.get('ensemble_prediction')}")
        print(f"Recommendation: {recommendation}")
        print("\nTraining performance of models:")
        for model, results in training_results.items():
            if 'rmse' in results:
                print(f"  - {model}: RMSE = {results['rmse']:.2f}, Best Params: {results.get('best_params', {})}")

        print("\n--- Verification Succeeded ---")

    except Exception as e:
        print(f"\n--- Verification FAILED ---")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_verification_test()
