@echo off
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found on PATH.
    echo Install it from https://www.python.org/downloads/
    echo and make sure to check "Add python.exe to PATH" during setup.
    pause
    exit /b 1
)

python -c "import flask" >nul 2>nul
if errorlevel 1 (
    echo Installing Flask...
    pip install -r requirements.txt
)

start "CustomAnswerAI" cmd /k python app.py

echo Starting the server, please wait...
timeout /t 2 /nobreak >nul
start http://localhost:5000

echo.
echo Started. Address: http://localhost:5000
echo To stop it, double-click stop.bat
pause
