#!/usr/bin/env python3
"""
Combined startup script for both API and frontend
"""

import subprocess
import sys
import os
import time
import signal
import webbrowser
from threading import Timer

def open_browser():
    """Open the browser after a short delay"""
    webbrowser.open('http://localhost:3000')

def run_app():
    """Run both API and frontend servers"""
    print("🚀 Starting Stock Prediction Dashboard...")
    print("=" * 60)
    
    # Start API server
    print("📡 Starting API server...")
    api_process = subprocess.Popen([
        sys.executable, 
        "-m", "uvicorn", 
        "src.api.main_fixed:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
        "--reload"
    ])
    
    # Wait a bit for API to start
    time.sleep(3)
    
    # Start frontend server
    print("🌐 Starting frontend server...")
    frontend_process = subprocess.Popen([
        sys.executable, 
        "serve_frontend.py"
    ])
    
    # Open browser after 2 seconds
    Timer(2, open_browser).start()
    
    print("✅ Both servers are running!")
    print("📊 Dashboard: http://localhost:3000")
    print("🔧 API Docs: http://localhost:8000/docs")
    print("💡 Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        # Wait for both processes
        api_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\\n🛑 Stopping servers...")
        
        # Terminate both processes
        api_process.terminate()
        frontend_process.terminate()
        
        # Wait for them to finish
        api_process.wait()
        frontend_process.wait()
        
        print("✅ All servers stopped successfully")

if __name__ == "__main__":
    run_app()
