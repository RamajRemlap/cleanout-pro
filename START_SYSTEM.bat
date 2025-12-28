@echo off
REM CleanoutPro - Start All Systems
REM Windows batch script to launch backend, mobile, and desktop apps

echo ========================================
echo   CleanoutPro System Launcher
echo ========================================
echo.

REM Check if backend is running
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend already running at http://localhost:8000
) else (
    echo [STARTING] Backend API...
    start "CleanoutPro Backend" cmd /k "cd backend && venv\Scripts\activate && python api/main.py"
    timeout /t 5 /nobreak >nul
)

echo.
echo ========================================
echo   Choose what to start:
echo ========================================
echo   1. Mobile App (React Native)
echo   2. Desktop App (Electron)
echo   3. Lead Generator (Michigan Jobs)
echo   4. All Components
echo   5. Exit
echo ========================================
echo.

set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto mobile
if "%choice%"=="2" goto desktop
if "%choice%"=="3" goto leads
if "%choice%"=="4" goto all
if "%choice%"=="5" goto end

:mobile
echo.
echo [STARTING] Mobile App Metro Bundler...
start "CleanoutPro Mobile" cmd /k "cd mobile && npm start"
echo.
echo Mobile app Metro bundler started!
echo Run 'npm run android' or 'npm run ios' in mobile directory
goto end

:desktop
echo.
echo [STARTING] Desktop App...
start "CleanoutPro Desktop" cmd /k "cd desktop && npm start"
echo.
echo Desktop app started!
goto end

:leads
echo.
echo [STARTING] Lead Generator...
start "CleanoutPro Leads" cmd /k "cd backend && venv\Scripts\activate && python services/michigan_lead_generator.py"
echo.
echo Lead generator started! Check michigan_leads.db for results
goto end

:all
echo.
echo [STARTING] All Components...
start "CleanoutPro Mobile" cmd /k "cd mobile && npm start"
timeout /t 2 /nobreak >nul
start "CleanoutPro Desktop" cmd /k "cd desktop && npm start"
timeout /t 2 /nobreak >nul
start "CleanoutPro Leads" cmd /k "cd backend && venv\Scripts\activate && python services/michigan_lead_generator.py"
echo.
echo All components started!
goto end

:end
echo.
echo ========================================
echo   System Status:
echo ========================================
echo   Backend:  http://localhost:8000/docs
echo   Mobile:   Metro bundler running
echo   Desktop:  Electron app running
echo ========================================
echo.
pause
