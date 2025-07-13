#!/usr/bin/env python3
"""
Startup script for the Stock Prediction API server
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

if __name__ == "__main__":
    print("Starting Stock Prediction API server...")
    print("Visit: http://localhost:8000")
    print("API docs: http://localhost:8000/docs") 
    print("Health check: http://localhost:8000/health")
    print("\nAvailable endpoints:")
    print("- GET /health - Health check")
    print("- GET /stocks/{symbol} - Technical analysis")
    print("- GET /company/{symbol} - Fundamental analysis")
    print("- GET /predict/{symbol} - Price prediction")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "src.api.main_fixed:app",
            host="127.0.0.1",
            port=8000,
            log_level="info",
            reload=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
