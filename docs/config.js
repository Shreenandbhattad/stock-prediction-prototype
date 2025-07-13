// Configuration for different environments
const config = {
    development: {
        API_BASE_URL: 'http://localhost:8000'
    },
    production: {
        // Replace with your deployed API URL (e.g., Heroku, AWS, etc.)
        API_BASE_URL: 'https://your-api-domain.herokuapp.com'
    }
};

// Auto-detect environment
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const currentConfig = isDevelopment ? config.development : config.production;

// Export configuration
window.APP_CONFIG = currentConfig;
