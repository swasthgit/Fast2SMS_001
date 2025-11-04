#!/bin/bash

# Fast2SMS Bulk Sender - Run Script (Linux/Mac)

echo "=================================="
echo "Fast2SMS Bulk Sender Web App"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
    echo "Dependencies installed!"
    echo ""
fi

# Run the application
echo "Starting Fast2SMS Bulk Sender..."
echo ""
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
