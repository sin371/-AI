@echo off
chcp 65001 >nul
taskkill /FI "WINDOWTITLE eq CustomAnswerAI" /T /F >nul 2>nul
if errorlevel 1 (
    echo 실행 중인 서버를 찾지 못했습니다. 이미 종료되었을 수 있습니다.
) else (
    echo 종료되었습니다.
)
pause
