@echo off
cls
echo ========================================
echo             Rocore Scraper
echo ========================================

:: Check if Python is installed
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not added to the system PATH.
    echo Please install Python first: https://www.python.org/downloads/
    pause
    exit /b
)

:: Check if pip is installed
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)

:: Install required packages
echo Installing required packages...
pip install -r requirements.txt

:: Check if the installation was successful
if %errorlevel% neq 0 (
    echo ERROR: Failed to install the required packages.
    pause
    exit /b
)

:: Run the Python script
echo Running the Roblox User ID Scraper...
python Scraper.py

pause
