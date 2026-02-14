import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure we are running from the root directory
    sys.path.append(os.getcwd())
    
    print("Starting Assistive Vision Web Server...")
    print("Open http://localhost:8000 in your browser.")
    
    uvicorn.run("src.web_server:app", host="0.0.0.0", port=8000, reload=True)
