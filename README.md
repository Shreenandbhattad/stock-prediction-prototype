# Stock Prediction Prototype

A comprehensive AI-powered stock analysis and prediction system implementing advanced technical and fundamental analysis with machine learning models for stock price prediction and trading signal generation.

## Author

Developed by Shreenand Bhattad

## System Overview

The Stock Prediction Prototype is a full-stack financial analysis system that combines technical indicators, fundamental analysis, and machine learning algorithms to provide comprehensive stock analysis and predictions. The system architecture consists of a Python-based backend API deployed on Railway and a JavaScript frontend deployed on GitHub Pages.

## Live Application

- **Frontend Dashboard**: https://shreenandbhattad.github.io/stock-prediction-prototype/
- **Backend API**: https://stock-prediction-prototype-production.up.railway.app
- **API Documentation**: https://stock-prediction-prototype-production.up.railway.app/docs

## Technical Architecture

### Backend Infrastructure

**Platform**: Railway (Cloud Deployment)
**Framework**: FastAPI (Python)
**Database**: PostgreSQL
**Caching**: Redis
**API Documentation**: OpenAPI/Swagger

### Frontend Infrastructure

**Platform**: GitHub Pages (Static Hosting)
**Framework**: Vanilla JavaScript
**Styling**: CSS3 with responsive design
**Charts**: Chart.js for data visualization
**Build Tools**: Webpack for bundling

### Data Sources

**Primary Market Data**: Twelve Data API
**Supplementary Data**: Yahoo Finance (yfinance)
**Company Fundamentals**: Financial statement data
**Economic Data**: Interest rates, inflation, GDP growth
**News Sentiment**: Company-specific news analysis

## Core Features

### Technical Analysis Engine

The system implements over 30 technical indicators across multiple categories:

**Trend Indicators**:
- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Weighted Moving Average (WMA)
- Moving Average Convergence Divergence (MACD)
- Average Directional Index (ADX)
- Parabolic SAR
- Ichimoku Cloud

**Momentum Indicators**:
- Relative Strength Index (RSI)
- Stochastic Oscillator
- Williams %R
- Momentum Oscillator
- Rate of Change (ROC)

**Volume Indicators**:
- On-Balance Volume (OBV)
- Volume Weighted Average Price (VWAP)
- Accumulation/Distribution Line
- Chaikin Money Flow
- Volume Rate of Change

**Volatility Indicators**:
- Bollinger Bands
- Average True Range (ATR)
- Standard Deviation
- Volatility Index

### Fundamental Analysis System

The system analyzes over 40 fundamental metrics categorized as follows:

**Profitability Ratios**:
- Return on Equity (ROE)
- Return on Assets (ROA)
- Gross Margin
- Operating Margin
- Net Margin
- Return on Invested Capital (ROIC)

**Liquidity Ratios**:
- Current Ratio
- Quick Ratio
- Cash Ratio
- Working Capital

**Leverage Ratios**:
- Debt-to-Equity
- Interest Coverage Ratio
- Debt Service Coverage
- Equity Multiplier

**Efficiency Ratios**:
- Asset Turnover
- Inventory Turnover
- Receivables Turnover
- Fixed Asset Turnover

**Valuation Metrics**:
- Price-to-Earnings (P/E) Ratio
- Price-to-Book (P/B) Ratio
- Price-to-Sales (P/S) Ratio
- Enterprise Value to EBITDA (EV/EBITDA)
- Price/Earnings to Growth (PEG) Ratio
- Dividend Yield

**Growth Metrics**:
- Revenue Growth (Year-over-Year, Quarter-over-Quarter)
- Earnings Growth
- Book Value Growth
- Cash Flow Growth

### Financial Health Scoring

**Altman Z-Score**: Bankruptcy prediction model
**Piotroski F-Score**: Financial strength assessment (0-9 scale)
**Beneish M-Score**: Earnings manipulation detection
**Custom Health Score**: Weighted combination of key financial metrics

### Machine Learning Prediction Models

The system employs an ensemble approach using multiple algorithms:

**Base Models**:
- Linear Regression: Baseline trend analysis
- Random Forest: Feature importance and non-linear relationships
- XGBoost: Gradient boosting for complex patterns
- Support Vector Regression: Non-linear price movements
- LSTM Neural Network: Time-series pattern recognition
- ARIMA: Statistical time-series forecasting
- Prophet: Seasonal trend forecasting

**Ensemble Model**: Weighted combination of all models for improved accuracy

**Feature Engineering**: The system uses over 100 features including:
- All technical indicators
- All fundamental ratios
- Price momentum features
- Volume patterns
- Volatility measures
- Market sentiment scores
- Economic indicators
- Seasonal patterns
- Cross-asset correlations

### Prediction Outputs

**Price Predictions**:
- 1-Month Target Price
- 3-Month Target Price
- 6-Month Target Price
- 1-Year Target Price
- Confidence Intervals (90%, 80%, 70%)

**Risk Assessment**:
- Volatility Forecast
- Drawdown Risk
- Beta Coefficient
- Sharpe Ratio

### Decision Engine

The system generates trading recommendations based on:

**Technical Score** (0-100): Weighted combination of technical indicators
**Fundamental Score** (0-100): Financial health and valuation metrics
**Sentiment Score** (0-100): News and market sentiment analysis
**Risk Score** (0-100): Overall risk assessment

**Recommendations**:
- BUY: Strong positive signals across multiple models
- SELL: Strong negative signals, overvalued conditions
- HOLD: Mixed signals, fair value assessment
- AVOID: High risk, poor fundamentals

## Installation and Setup

### Prerequisites

**Python 3.8+**
**Node.js 14+** (for frontend development)
**PostgreSQL 12+** (for database)
**Redis 6+** (for caching)

### Local Development Setup

1. **Clone the repository**:
```bash
git clone https://github.com/shreenandbhattad/stock-prediction-prototype.git
cd stock-prediction-prototype
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.template .env
# Edit .env with your API keys and database credentials
```

4. **Start the application**:
```bash
python run_full_app.py
```

### Production Deployment

**Backend (Railway)**:
1. Connect your GitHub repository to Railway
2. Configure environment variables in Railway dashboard
3. Deploy using the provided Procfile

**Frontend (GitHub Pages)**:
1. Push changes to the main branch
2. GitHub Actions will automatically deploy to GitHub Pages

## API Documentation

### Authentication

The API uses API key authentication. Include your API key in the header:
```
Authorization: Bearer YOUR_API_KEY
```

### Core Endpoints

**GET /stocks/{symbol}**
- Description: Retrieve comprehensive technical analysis
- Parameters: symbol (string) - Stock ticker symbol
- Response: Technical indicators, trend analysis, trading signals

**GET /company/{symbol}**
- Description: Retrieve fundamental analysis and company information
- Parameters: symbol (string) - Stock ticker symbol
- Response: Financial ratios, company metrics, health scores

**GET /predict/{symbol}**
- Description: Generate ML-based price predictions
- Parameters: symbol (string) - Stock ticker symbol
- Response: Price targets, confidence intervals, recommendations

**GET /health**
- Description: System health check
- Response: Service status, database connectivity, API availability

### Response Format

All API responses follow a consistent JSON structure:
```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "metadata": {
    "timestamp": "2024-01-01T00:00:00Z",
    "processing_time": 0.123,
    "version": "1.0.0"
  }
}
```

## Usage Instructions

### Web Interface

1. **Access the dashboard**: Navigate to https://shreenandbhattad.github.io/stock-prediction-prototype/
2. **Enter stock symbol**: Input a valid stock ticker (e.g., AAPL, TSLA, MSFT)
3. **Analyze stock**: Click "Analyze Stock" for technical and fundamental analysis
4. **Get predictions**: Click "Get AI Prediction" for machine learning predictions
5. **Review results**: Examine comprehensive analysis including charts and recommendations

### API Integration

```python
import requests

# Example API call
response = requests.get(
    "https://stock-prediction-prototype-production.up.railway.app/stocks/AAPL",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

data = response.json()
print(data)
```

### Command Line Interface

```bash
# Analyze a single stock
python -m src.cli analyze AAPL

# Generate predictions
python -m src.cli predict AAPL

# Run batch analysis
python -m src.cli batch --file stocks.txt
```

## System Performance

### Performance Metrics

**Response Time**: Average 2-5 seconds per analysis
**Throughput**: 100+ requests per minute
**Accuracy**: 60-70% directional accuracy for price predictions
**Uptime**: 99.9% availability

### Scalability

**Horizontal Scaling**: Load balancer with multiple API instances
**Caching**: Redis for frequently accessed data
**Database Optimization**: Indexed queries and connection pooling
**CDN**: Static assets served via CDN

## Data Processing Pipeline

### Data Collection

1. **Market Data Ingestion**: Real-time price and volume data
2. **Fundamental Data Processing**: Financial statement analysis
3. **News Sentiment Analysis**: Natural language processing
4. **Economic Data Integration**: Macroeconomic indicators

### Data Validation

1. **Quality Checks**: Data completeness and accuracy validation
2. **Outlier Detection**: Statistical anomaly identification
3. **Missing Data Handling**: Interpolation and forward-fill techniques
4. **Data Normalization**: Standardization across different time periods

### Feature Engineering

1. **Technical Indicators**: Calculation of all technical metrics
2. **Fundamental Ratios**: Computation of financial ratios
3. **Time Series Features**: Lag variables and rolling statistics
4. **Cross-Asset Features**: Correlation and relative strength metrics

## Security Implementation

### API Security

**Authentication**: JWT token-based authentication
**Rate Limiting**: 1000 requests per hour per API key
**Input Validation**: Comprehensive input sanitization
**HTTPS**: All communications encrypted with TLS 1.3

### Data Security

**Database Encryption**: AES-256 encryption at rest
**Secure Transmission**: End-to-end encryption
**Access Control**: Role-based access permissions
**Audit Logging**: Complete audit trail for all operations

## Configuration Management

### Environment Variables

```bash
# API Configuration
TWELVE_DATA_API_KEY=your_api_key
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port

# ML Model Configuration
MODEL_ENSEMBLE_WEIGHTS=0.2,0.3,0.5
PREDICTION_HORIZON=365
CONFIDENCE_THRESHOLD=0.8

# System Configuration
LOG_LEVEL=INFO
MAX_CONCURRENT_REQUESTS=100
CACHE_TTL=3600
```

### Model Configuration

```json
{
  "technical_indicators": {
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "bollinger_period": 20
  },
  "fundamental_weights": {
    "profitability": 0.3,
    "liquidity": 0.2,
    "leverage": 0.2,
    "efficiency": 0.15,
    "valuation": 0.15
  },
  "ml_models": {
    "linear_regression": {"weight": 0.1},
    "random_forest": {"weight": 0.2, "n_estimators": 100},
    "xgboost": {"weight": 0.25, "max_depth": 6},
    "lstm": {"weight": 0.25, "sequence_length": 60},
    "arima": {"weight": 0.1},
    "prophet": {"weight": 0.1}
  }
}
```

## Error Handling

### Error Codes

**400 Bad Request**: Invalid input parameters
**401 Unauthorized**: Missing or invalid API key
**404 Not Found**: Stock symbol not found
**429 Too Many Requests**: Rate limit exceeded
**500 Internal Server Error**: System error
**503 Service Unavailable**: Temporary service interruption

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": 400,
    "message": "Invalid stock symbol",
    "details": "Symbol must be a valid ticker (e.g., AAPL)"
  },
  "metadata": {
    "timestamp": "2024-01-01T00:00:00Z",
    "request_id": "req_123456789"
  }
}
```

## Testing

### Unit Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test category
python -m pytest tests/test_technical_analysis.py
python -m pytest tests/test_fundamental_analysis.py
python -m pytest tests/test_ml_models.py
```

### Integration Tests

```bash
# Test API endpoints
python -m pytest tests/integration/

# Test data pipeline
python -m pytest tests/integration/test_data_pipeline.py
```

### Load Testing

```bash
# Performance testing
locust -f tests/load/locustfile.py --host=https://stock-prediction-prototype-production.up.railway.app
```

## Monitoring and Logging

### Application Monitoring

**Metrics Collection**: Prometheus for metrics gathering
**Log Aggregation**: Centralized logging with structured format
**Performance Tracking**: Response time and throughput monitoring
**Error Tracking**: Comprehensive error reporting and alerting

### Log Format

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "INFO",
  "service": "stock-prediction-api",
  "message": "Analysis completed for AAPL",
  "metadata": {
    "symbol": "AAPL",
    "processing_time": 2.345,
    "user_id": "user_123"
  }
}
```

## Maintenance and Updates

### Model Retraining

**Schedule**: Monthly retraining of ML models
**Data Requirements**: Minimum 2 years of historical data
**Validation**: Backtesting against historical performance
**Deployment**: Automated model deployment with A/B testing

### System Updates

**Dependencies**: Regular security and performance updates
**API Versioning**: Backward-compatible API evolution
**Database Migration**: Automated schema updates
**Configuration Management**: Version-controlled configuration

## Performance Optimization

### Caching Strategy

**API Response Caching**: 15-minute TTL for analysis results
**Database Query Caching**: Optimized query result storage
**Static Asset Caching**: CDN-based asset delivery
**Memory Caching**: In-memory storage for frequently accessed data

### Database Optimization

**Indexing**: Optimized database indexes for query performance
**Partitioning**: Time-based table partitioning
**Connection Pooling**: Efficient database connection management
**Query Optimization**: Optimized SQL queries and stored procedures

## Troubleshooting

### Common Issues

**API Timeout**: Increase request timeout or check system status
**Invalid Stock Symbol**: Verify ticker symbol is valid and supported
**Rate Limit Exceeded**: Implement request throttling or upgrade plan
**Data Unavailable**: Check data source availability and API keys

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python start_server.py
```

### Health Checks

```bash
# Check API health
curl https://stock-prediction-prototype-production.up.railway.app/health

# Check database connectivity
curl https://stock-prediction-prototype-production.up.railway.app/health/database
```

## Contributing

This project is developed and maintained by Shreenand Bhattad. For issues or suggestions, please create an issue in the GitHub repository.

### Development Guidelines

**Code Style**: PEP 8 for Python, ESLint for JavaScript
**Documentation**: Comprehensive docstrings and comments
**Testing**: Unit tests required for all new features
**Version Control**: Git flow with feature branches

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer

This system is designed for educational and research purposes. All predictions and recommendations are based on historical data and mathematical models. Stock trading involves significant financial risk, and users should conduct their own research and consult with financial advisors before making investment decisions. The author assumes no responsibility for financial losses resulting from the use of this system.

## Support

For technical support, bug reports, or feature requests, please contact:

**Developer**: Shreenand Bhattad
**Repository**: https://github.com/shreenandbhattad/stock-prediction-prototype
**Issues**: https://github.com/shreenandbhattad/stock-prediction-prototype/issues

---

**Version**: 1.0.0
**Last Updated**: January 2024
**Build Status**: Production Ready
