"""
Main FastAPI application to run the stock prediction service.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Initialize FastAPI
app = FastAPI(title="Stock Prediction Prototype")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Stock Prediction API is running!", "status": "healthy"}

@app.get("/health", summary="Get service health status", tags=["Health"])
def get_health_status():
    """
    Endpoint to check the health status of the API
    """
    return {"status": "healthy"}

@app.get("/stocks/{symbol}", summary="Get stock analysis", tags=["Stocks"])
def get_stock_analysis(symbol: str):
    """
    Endpoint to get stock analysis for a given symbol
    """
    try:
        from src.data.marketstack import marketstack_client
        from src.analysis.technical_indicators import calculate_all_indicators, get_technical_summary
        
        # Fetch stock data
        stock_data = marketstack_client.get_stock_data(symbol)
        if stock_data.empty:
            raise HTTPException(status_code=404, detail="Stock data not found")
        
        # Calculate technical indicators
        indicators = calculate_all_indicators(stock_data)

        # Get technical summary
        tech_summary = get_technical_summary(indicators)

        return {
            "symbol": symbol,
            "technical_summary": tech_summary,
            "indicators": indicators.to_dict(orient='records')[-1] # latest indicators
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}

@app.get("/company/{symbol}", summary="Get company info and fundamental analysis", tags=["Company"])
def get_company_analysis(symbol: str):
    """
    Endpoint to get company info and fundamental analysis for a given symbol
    """
    try:
        from src.analysis.fundamental import get_fundamental_summary
        
        # Get company info and fundamental metrics
        fundamental_summary = get_fundamental_summary(symbol)
        
        return fundamental_summary
    except Exception as e:
        return {"error": str(e), "symbol": symbol}

@app.get("/predict/{symbol}", summary="Predict stock price", tags=["Prediction"])
def predict_stock_price(symbol: str, days: int = 30):
    """
    Endpoint to predict future stock prices for a given symbol
    """
    try:
        from src.data.marketstack import marketstack_client
        from src.analysis.technical_indicators import calculate_all_indicators
        from src.prediction.ml_models import StockPredictor, create_ensemble_prediction, generate_recommendation
        
        # Fetch stock data and calculate indicators
        stock_data = marketstack_client.get_stock_data(symbol)
        if stock_data.empty:
            raise HTTPException(status_code=404, detail="Stock data not found")
        
        indicators = calculate_all_indicators(stock_data)

        # Prepare features and train models
        predictor = StockPredictor()
        X, y = predictor.prepare_features(indicators)
        training_results = predictor.train_models(X, y)
        
        # Predict future prices
        future_predictions = predictor.predict_future(indicators, days=days)
        
        # Create ensemble prediction
        ensemble_result = create_ensemble_prediction(future_predictions)

        # Current price
        current_price = indicators.iloc[-1]['close']

        # Generate recommendation
        recommendation = generate_recommendation(current_price, 
                                                 ensemble_result.get('ensemble_prediction', current_price), 
                                                 ensemble_result.get('confidence', 0.5))

        return {
            "symbol": symbol,
            "training_results": training_results,
            "future_predictions": future_predictions,
            "ensemble_prediction": ensemble_result,
            "recommendation": recommendation,
            "current_price": current_price
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}
