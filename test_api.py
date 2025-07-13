"""
Simple test API to diagnose server issues
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Stock Prediction Test API")

@app.get("/")
def read_root():
    return {"message": "Stock Prediction API is running!", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is working"}

if __name__ == "__main__":
    print("Starting test API server...")
    print("Visit: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
