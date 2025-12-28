@echo off
REM Monitor LLaVA AI Model Download Progress

echo ========================================
echo   LLaVA AI Model Download Monitor
echo ========================================
echo.

:loop
cls
echo ========================================
echo   LLaVA AI Model Download Monitor
echo ========================================
echo.

REM Check if ollama is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [RUNNING] Ollama service is running
) else (
    echo [STOPPED] Ollama service is not running
    echo.
    echo Start Ollama with: ollama serve
    goto end
)

echo.
echo Checking download status...
echo.

REM Get list of models
ollama list 2>&1 | findstr /i "llava" >nul
if %errorlevel% equ 0 (
    echo [COMPLETE] LLaVA model is installed!
    echo.
    ollama list | findstr /i "llava"
    echo.
    echo ========================================
    echo   Download Complete!
    echo ========================================
    echo.
    echo You can now use AI vision classification.
    echo Test it with:
    echo   cd backend
    echo   python -c "from services.ai_vision import get_ai_vision_service; print(get_ai_vision_service().test_connection())"
    goto end
) else (
    echo [DOWNLOADING] LLaVA model is still downloading...
    echo.
    echo Current models installed:
    ollama list
    echo.
    echo ----------------------------------------
    echo The download is running in background.
    echo This window will refresh every 10 seconds.
    echo Press Ctrl+C to stop monitoring.
    echo ----------------------------------------
)

echo.
timeout /t 10 /nobreak >nul
goto loop

:end
echo.
pause
