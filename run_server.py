#!/usr/bin/env python3
"""
Startup script for the Stock Prediction API server
"""

import uvicorn

if __name__ == "__main__":
    print("Starting Stock Prediction API server...")
    print("Access the API documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "src.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
