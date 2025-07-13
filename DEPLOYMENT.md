# Deployment Guide

## GitHub Pages Frontend Deployment

### Step 1: Prepare Repository
1. Create a new GitHub repository
2. Push your entire project to the repository

### Step 2: Deploy API Backend
Since GitHub Pages only supports static files, you need to deploy your API separately:

**Option A: Heroku (Recommended)**
1. Install Heroku CLI
2. Create a Procfile:
```
web: python -m uvicorn src.api.main_fixed:app --host 0.0.0.0 --port $PORT
```
3. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

**Option B: Railway**
1. Connect your GitHub repo to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically

**Option C: Render**
1. Connect your GitHub repo to Render
2. Set up web service with start command:
```
python -m uvicorn src.api.main_fixed:app --host 0.0.0.0 --port $PORT
```

### Step 3: Update Frontend Configuration
1. Edit `frontend/config.js`
2. Replace `https://your-api-domain.herokuapp.com` with your actual API URL
3. Example:
```javascript
production: {
    API_BASE_URL: 'https://your-stock-api.herokuapp.com'
}
```

### Step 4: Deploy Frontend to GitHub Pages
1. Go to your GitHub repository
2. Navigate to Settings → Pages
3. Select "Deploy from a branch"
4. Choose "main" branch and "/frontend" folder
5. Click Save

### Step 5: Access Your Application
- Your frontend will be available at: `https://yourusername.github.io/your-repo-name/`
- API will be running at your chosen hosting service

## Environment Variables for API Deployment

Set these environment variables in your hosting service:

```
MARKETSTACK_API_KEY=102b76768338d536bf46fb894114cf29
MARKETSTACK_BASE_URL=http://api.marketstack.com/v1
MODEL_CACHE_DURATION=86400
RETRAIN_INTERVAL=604800
PREDICTION_CONFIDENCE_THRESHOLD=0.6
API_HOST=0.0.0.0
API_PORT=8000
```

## Local Development vs Production

### Local Development
- API runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- Use `python run_full_app.py` to start both

### Production
- API runs on your hosting service
- Frontend runs on GitHub Pages
- Automatic environment detection in `config.js`

## Troubleshooting

### CORS Issues
If you encounter CORS errors:
1. Ensure CORS middleware is properly configured in your API
2. Check that your API URL is correct in `config.js`
3. Verify your API is accessible from the browser

### API Connection Issues
1. Check your API is running and accessible
2. Verify the API URL in production config
3. Check browser console for error messages

### GitHub Pages Build Issues
1. Ensure all files are in the `frontend` folder
2. Check that all paths are relative
3. Verify no server-side code is in the frontend

## Features in Production

✅ **Working Features:**
- Real-time stock analysis
- Technical indicators with charts
- Advanced ML models (Linear Regression, Random Forest, SVR)
- Beautiful responsive dashboard
- Trading signals and recommendations

⚠️ **Limited Features (require additional setup):**
- XGBoost (install: `pip install xgboost`)
- LSTM Neural Networks (install: `pip install tensorflow`)
- ARIMA models (install: `pip install statsmodels`)

## Performance Optimization

### Frontend
- Charts are cached and reused
- API calls are optimized
- Responsive design for all devices

### Backend
- Model caching
- Efficient data processing
- Error handling and fallbacks

## Security Considerations

1. **API Keys**: Never expose API keys in frontend code
2. **HTTPS**: Always use HTTPS in production
3. **Rate Limiting**: Implement rate limiting on your API
4. **Input Validation**: Validate all user inputs

## Cost Considerations

- **GitHub Pages**: Free for public repositories
- **Heroku**: Free tier available with limitations
- **MarketStack API**: Free tier with request limits
- **Railway/Render**: Free tiers available

## Next Steps

1. Deploy your API to a hosting service
2. Update the frontend configuration
3. Push to GitHub and enable Pages
4. Test the full application
5. Monitor performance and errors

Your stock prediction dashboard will be fully functional and accessible to users worldwide!
