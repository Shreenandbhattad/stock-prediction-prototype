#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend
"""

import http.server
import socketserver
import os
import webbrowser
from threading import Timer

def open_browser():
    """Open the browser after a short delay"""
    webbrowser.open('http://localhost:3000')

def start_server():
    """Start the HTTP server"""
    PORT = 3000
    web_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # Change to the frontend directory
    os.chdir(web_dir)
    
    # Create handler
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Create server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Frontend server running at: http://localhost:{PORT}")
        print(f"Make sure the API server is running at: http://localhost:8000")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Open browser after 1 second
        Timer(1, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nFrontend server stopped")

if __name__ == "__main__":
    start_server()
