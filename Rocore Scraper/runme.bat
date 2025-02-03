@echo off
cls

:: Clear screen and display a nice banner
echo ================================================
echo        *** Rocore Scraper - Setup Process ***
echo ================================================

:: Adding some space for better readability
echo.

:: Check if Python is installed
echo Checking if Python is installed...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not added to the system PATH.
    echo Please install Python first: https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

:: Check if pip is installed
echo Checking if pip is installed...
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ERROR: pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)

:: Installing required packages
echo Installing required packages...
echo -----------------------------------------------
pip install -r requirements.txt
echo -----------------------------------------------

:: Check if the installation was successful
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install the required packages.
    pause
    exit /b
)

:: Run the Python script
echo Running the Roblox User ID Scraper...
echo -----------------------------------------------
python Scraper.py
echo -----------------------------------------------

:: Pause before exit for final message
echo.
echo *** Setup Complete! ***
pause
