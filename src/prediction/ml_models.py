"""
Machine learning models for stock price prediction.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Dict, Tuple, List, Any
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost not available. Install with: pip install xgboost")

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available. Install with: pip install tensorflow")

try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.seasonal import seasonal_decompose
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    print("Statsmodels not available. Install with: pip install statsmodels")

class StockPredictor:
    """Stock price prediction using multiple ML models"""
    
    def __init__(self):
        self.models = {
            'linear_regression': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'svr': SVR(kernel='rbf', C=1.0, epsilon=0.1)
        }
        
        # Add XGBoost if available
        if XGBOOST_AVAILABLE:
            self.models['xgboost'] = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        
        self.scaler = StandardScaler()
        self.lstm_scaler = MinMaxScaler()
        self.is_fitted = False
        self.lstm_model = None
        self.arima_model = None
        self.model_descriptions = {
            'linear_regression': 'Linear Regression - Basic trend analysis using linear relationships',
            'random_forest': 'Random Forest - Ensemble method using multiple decision trees',
            'svr': 'Support Vector Regression - Non-linear pattern recognition with RBF kernel',
            'xgboost': 'XGBoost - Gradient boosting with advanced regularization',
            'lstm': 'LSTM Neural Network - Deep learning for time series patterns',
            'arima': 'ARIMA - Statistical time series forecasting model'
        }
        
    def prepare_features(self, df: pd.DataFrame, target_col: str = 'close') -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features for machine learning
        
        Args:
            df: DataFrame with stock data and technical indicators
            target_col: Target column name
            
        Returns:
            Tuple of (features, target)
        """
        # Create feature columns
        feature_columns = [
            'open', 'high', 'low', 'volume',
            'SMA_20', 'SMA_50', 'EMA_12', 'EMA_26',
            'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram',
            'BB_Upper', 'BB_Middle', 'BB_Lower',
            'Stoch_K', 'Stoch_D', 'ATR', 'ADX',
            'OBV', 'VWAP', 'Williams_R'
        ]
        
        # Add price-based features
        df['Price_Change'] = df[target_col].pct_change()
        df['Price_Change_5d'] = df[target_col].pct_change(5)
        df['Price_Change_10d'] = df[target_col].pct_change(10)
        df['Volume_Change'] = df['volume'].pct_change()
        
        # Add rolling statistics
        df['Price_Volatility'] = df[target_col].rolling(window=20).std()
        df['Volume_SMA'] = df['volume'].rolling(window=20).mean()
        
        # Add lag features
        for lag in [1, 2, 3, 5, 10]:
            df[f'Price_Lag_{lag}'] = df[target_col].shift(lag)
            df[f'Volume_Lag_{lag}'] = df['volume'].shift(lag)
        
        # Update feature columns
        feature_columns.extend([
            'Price_Change', 'Price_Change_5d', 'Price_Change_10d', 'Volume_Change',
            'Price_Volatility', 'Volume_SMA'
        ])
        
        for lag in [1, 2, 3, 5, 10]:
            feature_columns.extend([f'Price_Lag_{lag}', f'Volume_Lag_{lag}'])
        
        # Select features that exist in the dataframe
        available_features = [col for col in feature_columns if col in df.columns]
        
        # Drop rows with NaN values
        df_clean = df[available_features + [target_col]].dropna()
        
        X = df_clean[available_features]
        y = df_clean[target_col]
        
        return X, y
    
    def train_models(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Train all ML models
        
        Args:
            X: Features
            y: Target values
            
        Returns:
            Dictionary with training results
        """
        if len(X) < 50:
            raise ValueError("Not enough data points for training. Need at least 50 samples.")
        
        # Split data (80% train, 20% test)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        results = {}
        
        # Train each model
        for model_name, model in self.models.items():
            try:
                # Train model
                model.fit(X_train_scaled, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test_scaled)
                
                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                results[model_name] = {
                    'mse': mse,
                    'mae': mae,
                    'r2': r2,
                    'rmse': np.sqrt(mse)
                }
                
            except Exception as e:
                results[model_name] = {
                    'error': str(e)
                }
        
        # Train LSTM model if TensorFlow is available
        if TENSORFLOW_AVAILABLE:
            try:
                lstm_results = self.train_lstm_model(df, target_col)
                results['lstm'] = lstm_results
            except Exception as e:
                results['lstm'] = {'error': str(e)}
        
        # Train ARIMA model if statsmodels is available
        if STATSMODELS_AVAILABLE:
            try:
                arima_results = self.train_arima_model(df[target_col])
                results['arima'] = arima_results
            except Exception as e:
                results['arima'] = {'error': str(e)}
        
        self.is_fitted = True
        return results
    
    def predict(self, X: pd.DataFrame) -> Dict[str, np.ndarray]:
        """
        Make predictions with all models
        
        Args:
            X: Features for prediction
            
        Returns:
            Dictionary with predictions from each model
        """
        if not self.is_fitted:
            raise ValueError("Models must be trained first")
        
        X_scaled = self.scaler.transform(X)
        predictions = {}
        
        for model_name, model in self.models.items():
            try:
                pred = model.predict(X_scaled)
                predictions[model_name] = pred
            except Exception as e:
                predictions[model_name] = f"Error: {str(e)}"
        
        return predictions
    
    def predict_future(self, df: pd.DataFrame, days: int = 30) -> Dict[str, Any]:
        """
        Predict future stock prices
        
        Args:
            df: Historical data with features
            days: Number of days to predict
            
        Returns:
            Dictionary with predictions and confidence intervals
        """
        if not self.is_fitted:
            raise ValueError("Models must be trained first")
        
        # Get the latest data point
        latest_data = df.iloc[-1:].copy()
        
        predictions = {}
        
        for model_name, model in self.models.items():
            try:
                # Prepare features for the latest data point
                X_latest = latest_data[[col for col in latest_data.columns if col != 'close']].fillna(0)
                X_scaled = self.scaler.transform(X_latest)
                
                # Make prediction
                pred = model.predict(X_scaled)[0]
                
                # Simple confidence interval (using historical volatility)
                historical_volatility = df['close'].pct_change().std()
                confidence_interval = pred * historical_volatility * np.sqrt(days)
                
                predictions[model_name] = {
                    'prediction': pred,
                    'confidence_interval': confidence_interval,
                    'upper_bound': pred + confidence_interval,
                    'lower_bound': pred - confidence_interval
                }
                
            except Exception as e:
                predictions[model_name] = {
                    'error': str(e)
                }
        
        return predictions
    
    def train_lstm_model(self, df: pd.DataFrame, target_col: str, sequence_length: int = 60) -> Dict[str, Any]:
        """
        Train LSTM model for time series prediction
        """
        # Prepare data for LSTM
        data = df[target_col].values.reshape(-1, 1)
        scaled_data = self.lstm_scaler.fit_transform(data)
        
        # Create sequences
        X, y = [], []
        for i in range(sequence_length, len(scaled_data)):
            X.append(scaled_data[i-sequence_length:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        # Split data
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Build LSTM model
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(1))
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        # Train model
        model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
        
        # Make predictions
        predictions = model.predict(X_test)
        
        # Transform back to original scale
        predictions = self.lstm_scaler.inverse_transform(predictions)
        y_test_scaled = self.lstm_scaler.inverse_transform(y_test.reshape(-1, 1))
        
        # Calculate metrics
        mse = mean_squared_error(y_test_scaled, predictions)
        mae = mean_absolute_error(y_test_scaled, predictions)
        r2 = r2_score(y_test_scaled, predictions)
        
        self.lstm_model = model
        
        return {
            'mse': mse,
            'mae': mae,
            'r2': r2,
            'rmse': np.sqrt(mse)
        }
    
    def train_arima_model(self, series: pd.Series) -> Dict[str, Any]:
        """
        Train ARIMA model for time series prediction
        """
        # Prepare data
        train_size = int(len(series) * 0.8)
        train_data = series[:train_size]
        test_data = series[train_size:]
        
        # Fit ARIMA model (using auto-selected parameters)
        try:
            model = ARIMA(train_data, order=(1, 1, 1))
            fitted_model = model.fit()
            
            # Make predictions
            predictions = fitted_model.forecast(steps=len(test_data))
            
            # Calculate metrics
            mse = mean_squared_error(test_data, predictions)
            mae = mean_absolute_error(test_data, predictions)
            r2 = r2_score(test_data, predictions)
            
            self.arima_model = fitted_model
            
            return {
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'rmse': np.sqrt(mse)
            }
        except Exception as e:
            return {'error': str(e)}

def create_ensemble_prediction(predictions: Dict[str, Any]) -> Dict[str, float]:
    """
    Create ensemble prediction from multiple models
    
    Args:
        predictions: Dictionary of model predictions
        
    Returns:
        Ensemble prediction with confidence metrics
    """
    valid_predictions = []
    
    for model_name, pred_data in predictions.items():
        if isinstance(pred_data, dict) and 'prediction' in pred_data:
            valid_predictions.append(pred_data['prediction'])
    
    if not valid_predictions:
        return {'error': 'No valid predictions available'}
    
    # Simple ensemble: average of all predictions
    ensemble_prediction = np.mean(valid_predictions)
    prediction_std = np.std(valid_predictions)
    
    return {
        'ensemble_prediction': ensemble_prediction,
        'prediction_std': prediction_std,
        'confidence': max(0, min(1, 1 - prediction_std / ensemble_prediction)) if ensemble_prediction != 0 else 0,
        'num_models': len(valid_predictions)
    }

def generate_recommendation(current_price: float, predicted_price: float, confidence: float) -> str:
    """
    Generate buy/sell/hold recommendation
    
    Args:
        current_price: Current stock price
        predicted_price: Predicted stock price
        confidence: Prediction confidence (0-1)
        
    Returns:
        Recommendation string
    """
    if confidence < 0.5:
        return "HOLD"  # Low confidence
    
    price_change_pct = (predicted_price - current_price) / current_price
    
    if price_change_pct > 0.1 and confidence > 0.7:
        return "BUY"
    elif price_change_pct < -0.1 and confidence > 0.7:
        return "SELL"
    else:
        return "HOLD"
