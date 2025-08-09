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
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from typing import Dict, Tuple, List, Any
import warnings
import joblib
import os
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
    import pmdarima as pm
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    print("Statsmodels or pmdarima not available. Install with: pip install statsmodels pmdarima")

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

        # Add parameter grids for GridSearchCV
        self.param_grids = {
            'random_forest': {
                'n_estimators': [50, 100, 150],
                'max_depth': [5, 10, 20],
                'min_samples_leaf': [1, 2, 4]
            },
            'svr': {
                'C': [0.1, 1, 10],
                'epsilon': [0.1, 0.2]
            },
            'xgboost': {
                'n_estimators': [50, 100],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.05, 0.1]
            }
        }

        self.model_descriptions = {
            'linear_regression': 'Linear Regression - Basic trend analysis using linear relationships',
            'random_forest': 'Random Forest - Ensemble method using multiple decision trees',
            'svr': 'Support Vector Regression - Non-linear pattern recognition with RBF kernel',
            'xgboost': 'XGBoost - Gradient boosting with advanced regularization',
            'lstm': 'LSTM Neural Network - Deep learning for time series patterns',
            'arima': 'ARIMA - Statistical time series forecasting model'
        }

    def save(self, filepath: str, training_results: Dict[str, Any]):
        """Saves the trained models, scaler, and results to a file."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Save the important parts of the predictor
        joblib.dump({
            'models': self.models,
            'scaler': self.scaler,
            'lstm_scaler': self.lstm_scaler,
            'lstm_model': self.lstm_model,
            'arima_model': self.arima_model,
            'training_results': training_results # Save the results too
        }, filepath)
        print(f"Predictor saved to {filepath}")

    @classmethod
    def load(cls, filepath: str):
        """Loads a trained predictor from a file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No saved model found at {filepath}")

        data = joblib.load(filepath)

        # Create a new predictor instance
        predictor = cls()

        # Load the saved state
        predictor.models = data['models']
        predictor.scaler = data['scaler']
        predictor.lstm_scaler = data['lstm_scaler']
        predictor.lstm_model = data['lstm_model']
        predictor.arima_model = data['arima_model']
        predictor.training_results = data.get('training_results', {}) # Load results
        predictor.is_fitted = True

        print(f"Predictor loaded from {filepath}")
        return predictor
        
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
            'OBV', 'VWAP', 'Williams_R',
            # Fundamental features
            'Net_Margin', 'Debt_to_Equity', 'Current_Ratio',
            # Sentiment features
            'sentiment_avg'
        ]
        
        # Add price-based features
        df['Price_Change'] = df[target_col].pct_change()
        df['Price_Change_5d'] = df[target_col].pct_change(5)
        df['Price_Change_10d'] = df[target_col].pct_change(10)
        df['Volume_Change'] = df['volume'].pct_change()
        
        # Add rolling statistics
        df['Price_Volatility'] = df[target_col].rolling(window=10).std()
        df['Volume_SMA'] = df['volume'].rolling(window=10).mean()
        
        # Add lag features
        for lag in [1, 2, 3, 5]:
            df[f'Price_Lag_{lag}'] = df[target_col].shift(lag)
            df[f'Volume_Lag_{lag}'] = df['volume'].shift(lag)
        
        # Update feature columns
        feature_columns.extend([
            'Price_Change', 'Price_Change_5d', 'Price_Change_10d', 'Volume_Change',
            'Price_Volatility', 'Volume_SMA'
        ])
        
        for lag in [1, 2, 3, 5]:
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
        
        results = {}

        # Time series cross-validation
        tscv = TimeSeriesSplit(n_splits=3)

        # Train each model
        for model_name, model in self.models.items():
            try:
                print(f"    - Tuning {model_name}...")
                best_params = {}
                if model_name in self.param_grids:
                    # Perform GridSearchCV for models with a parameter grid
                    grid_search = GridSearchCV(
                        estimator=model,
                        param_grid=self.param_grids[model_name],
                        cv=tscv,
                        scoring='neg_mean_squared_error',
                        n_jobs=-1  # Use all available cores for offline training
                    )
                    grid_search.fit(X_train_scaled, y_train)

                    # Update the model to the best one found
                    self.models[model_name] = grid_search.best_estimator_
                    best_params = grid_search.best_params_

                    # Make predictions with the best model
                    y_pred = grid_search.predict(X_test_scaled)
                else:
                    # For models without a grid, like Linear Regression
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)

                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                results[model_name] = {
                    'mse': mse,
                    'mae': mae,
                    'r2': r2,
                    'rmse': np.sqrt(mse),
                    'best_params': best_params
                }
                
            except Exception as e:
                results[model_name] = {
                    'error': str(e)
                }
        
        # Train LSTM model if TensorFlow is available
        if TENSORFLOW_AVAILABLE:
            try:
                # We need the original dataframe for this, so we have to pass it
                # For now, let's pass `y` as it contains the target series
                lstm_results = self.train_lstm_model(y.to_frame(name='close'), 'close')
                results['lstm'] = lstm_results
            except Exception as e:
                results['lstm'] = {'error': str(e)}
        
        # Train ARIMA model if statsmodels is available
        if STATSMODELS_AVAILABLE:
            try:
                arima_results = self.train_arima_model(y)
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
        
        # Prepare features for the entire dataframe to get the latest row with all features
        X_full, _ = self.prepare_features(df.copy())

        if X_full.empty:
            return {"error": "Not enough data to generate features for prediction."}

        X_latest = X_full.iloc[-1:]
        X_scaled = self.scaler.transform(X_latest)
        
        predictions = {}
        
        for model_name, model in self.models.items():
            try:
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
            # Use auto_arima to find the best ARIMA model
            fitted_model = pm.auto_arima(
                train_data,
                start_p=1, start_q=1,
                max_p=3, max_q=3,
                seasonal=False,
                d=1,
                trace=False,
                error_action='ignore',
                suppress_warnings=True,
                stepwise=True
            )
            
            # Make predictions
            predictions = fitted_model.predict(n_periods=len(test_data))
            
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

def create_ensemble_prediction(predictions: Dict[str, Any], model_performance: Dict[str, Any]) -> Dict[str, float]:
    """
    Create a weighted ensemble prediction from multiple models based on their performance.
    
    Args:
        predictions: Dictionary of model predictions for the future.
        model_performance: Dictionary with performance metrics (like 'mse') for each model.
        
    Returns:
        Ensemble prediction with confidence metrics.
    """
    valid_predictions = []
    weights = []
    
    for model_name, pred_data in predictions.items():
        if isinstance(pred_data, dict) and 'prediction' in pred_data:
            perf = model_performance.get(model_name)
            if perf and 'mse' in perf and perf['mse'] > 0:
                valid_predictions.append(pred_data['prediction'])
                # Weight is inverse of MSE
                weights.append(1.0 / perf['mse'])

    if not valid_predictions:
        return {'error': 'No valid predictions available for ensembling'}

    # Normalize weights
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]

    # Weighted average for the prediction
    ensemble_prediction = np.average(valid_predictions, weights=normalized_weights)
    
    # Weighted standard deviation for confidence
    variance = np.average((np.array(valid_predictions) - ensemble_prediction)**2, weights=normalized_weights)
    prediction_std = np.sqrt(variance)
    
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
