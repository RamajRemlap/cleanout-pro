@echo off
REM Deploy CleanoutPro Mobile Web PWA to Netlify

echo ========================================
echo   CleanoutPro Mobile Web Deployer
echo ========================================
echo.

cd mobile-web

echo [1/4] Installing dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: npm install failed
    pause
    exit /b 1
)

echo.
echo [2/4] Building for production...
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [3/4] Deployment options:
echo.
echo   1. Drag & Drop (Easiest)
echo      - Open: https://app.netlify.com/drop
echo      - Drag the 'dist' folder
echo.
echo   2. Netlify CLI (Auto-deploy)
echo      - Run: netlify deploy --prod
echo.
echo   3. GitHub (Team collaboration)
echo      - Push to GitHub
echo      - Connect on Netlify dashboard
echo.

echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo   Built files are in: mobile-web\dist\
echo.
echo   Next steps:
echo   1. Go to https://app.netlify.com/drop
echo   2. Drag the 'dist' folder onto the page
echo   3. Get your URL instantly!
echo.
echo   OR install Netlify CLI:
echo      npm install -g netlify-cli
echo      netlify deploy --prod
echo.
echo ========================================
pause

REM Open Netlify Drop page
start https://app.netlify.com/drop

echo.
echo Opening Netlify Drop page in browser...
echo Drag the 'dist' folder to deploy!
