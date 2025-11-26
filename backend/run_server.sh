#!/bin/bash
# Start the resuMAX backend server with proper environment

# Set library path for WeasyPrint (macOS requirement)
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Activate virtual environment and start server
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
