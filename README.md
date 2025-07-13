# Stock Prediction Dashboard

A comprehensive AI-powered stock analysis and prediction system with technical indicators, fundamental analysis, and machine learning models.

## Features

🔍 **Technical Analysis**
- 30+ technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, etc.)
- Real-time trend and momentum scoring
- Trading signal detection

📊 **Fundamental Analysis**
- Financial ratios (P/E, P/B, ROE, ROA, etc.)
- Company information and metrics
- Financial health scores (Altman Z-Score, Piotroski F-Score)

🤖 **Machine Learning Predictions**
- Multiple ML models (Linear Regression, Random Forest)
- Ensemble predictions
- BUY/SELL/HOLD recommendations

🌐 **Beautiful Dashboard**
- Real-time stock analysis
- Interactive charts and metrics
- Responsive design
- Professional UI/UX

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd stock-prediction-prototype
```

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Run Everything at Once (Recommended)
```bash
python run_full_app.py
```

This will start both the API server and frontend, then automatically open your browser.

### Option 2: Run Servers Separately

**Terminal 1 - API Server:**
```bash
python start_server.py
```

**Terminal 2 - Frontend Server:**
```bash
python serve_frontend.py
```

## Access Points

- **Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## API Endpoints

- `GET /stocks/{symbol}` - Get technical analysis
- `GET /company/{symbol}` - Get fundamental analysis  
- `GET /predict/{symbol}` - Get ML predictions
- `GET /health` - Health check

## Example Usage

1. **Open the dashboard** at http://localhost:3000
2. **Enter a stock symbol** (e.g., AAPL, TSLA, MSFT)
3. **Click "Analyze Stock"** to get technical and fundamental analysis
4. **Click "Get AI Prediction"** for ML-based price predictions
5. **View the comprehensive analysis** including:
   - Current price and key metrics
   - Technical indicators
   - Fundamental ratios
   - AI recommendation (BUY/SELL/HOLD)
   - Trading signals

## Technical Indicators Included

- **Trend Indicators**: SMA, EMA, WMA, MACD, ADX
- **Momentum Indicators**: RSI, Stochastic, Williams %R
- **Volume Indicators**: OBV, VWAP
- **Volatility Indicators**: Bollinger Bands, ATR

## Machine Learning Models

- **Linear Regression**: Baseline trend analysis
- **Random Forest**: Advanced pattern recognition
- **Ensemble Method**: Combined predictions for better accuracy

## Data Sources

- **Market Data**: MarketStack API
- **Company Data**: Yahoo Finance (yfinance)
- **News Sentiment**: Built-in sentiment analysis

## Configuration

Edit the `.env` file to configure:
- API keys
- Database connections
- Model parameters
- Analysis settings

## Project Structure

```
stock-prediction-prototype/
├── src/
│   ├── api/           # FastAPI endpoints
│   ├── data/          # Data collection modules
│   ├── analysis/      # Technical & fundamental analysis
│   ├── prediction/    # ML models
│   └── reports/       # Report generation
├── frontend/          # Web dashboard
├── config/            # Configuration files
├── tests/             # Test files
└── requirements.txt   # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Disclaimer

This system is for educational and research purposes only. Do not use it for actual trading decisions without proper risk management and additional research. Stock trading involves significant risks.

## Support

For issues and questions, please create an issue in the repository or contact the development team.

---

**Made with ❤️ by the Stock Prediction Team**
