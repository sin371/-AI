@echo off
chcp 65001 >nul
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않거나 PATH에 등록되지 않았습니다.
    echo https://www.python.org/downloads/ 에서 설치할 때 아래 화면에서
    echo "Add python.exe to PATH" 체크박스를 반드시 체크해 주세요.
    pause
    exit /b 1
)

python -c "import flask" >nul 2>nul
if errorlevel 1 (
    echo Flask를 설치합니다...
    pip install -r requirements.txt
)

tasklist /FI "WINDOWTITLE eq CustomAnswerAI" 2>nul | find /I "cmd.exe" >nul
if not errorlevel 1 (
    echo 이미 실행 중입니다.
    start http://localhost:5000
    exit /b 0
)

start "CustomAnswerAI" cmd /k python app.py

echo 서버를 켜는 중입니다. 잠시 기다려 주세요...
timeout /t 2 /nobreak >nul
start http://localhost:5000

echo.
echo 실행되었습니다. 주소: http://localhost:5000
echo 종료하려면 stop.bat 을 더블클릭하세요.
pause
