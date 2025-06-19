import argparse
import os
import sys
from pathlib import Path

import uvicorn

def main():
    parser = argparse.ArgumentParser(description="Example - Python code execution environment")
    parser.add_argument("command", choices=["run"], help="Command to execute")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    if args.command == "run":
        # Ensure the static files directory exists
        static_dir = Path(__file__).parent / "static"
        if not static_dir.exists():
            print("Error: Static files not found. Please ensure the package is installed correctly.", file=sys.stderr)
            sys.exit(1)
            
        # Set environment variable for the static files path
        os.environ["EXAMPLE_STATIC_DIR"] = str(static_dir)
        
        # Import and run the FastAPI app
        uvicorn.run(
            "example.app:app",
            host=args.host,
            port=args.port,
            reload=False
        ) 