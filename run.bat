@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Installing Python...
    powershell -Command "& {Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe -OutFile python-installer.exe}"
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
)

REM Check if Python is now available
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python installation failed. Please check manually.
    pause
    exit /b 1
)

REM Run install.py to create venv and install dependencies
echo Creating virtual environment and installing dependencies...
python install.py

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Run the application
echo Starting the application...
python run.py

REM Deactivate the virtual environment
deactivate

pause
