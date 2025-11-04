@echo off
REM Fast2SMS Bulk Sender - Run Script (Windows)

echo ==================================
echo Fast2SMS Bulk Sender Web App
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\installed
    echo Dependencies installed!
    echo.
)

REM Run the application
echo Starting Fast2SMS Bulk Sender...
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
