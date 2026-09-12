@echo off
taskkill /FI "WINDOWTITLE eq CustomAnswerAI" /T /F >nul 2>nul
if errorlevel 1 (
    echo Could not find a running server. It may already be stopped.
) else (
    echo Stopped.
)
pause
