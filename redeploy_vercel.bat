@echo off
echo ========================================
echo   Vercel Redeploy Script
echo ========================================
echo.

cd backend

echo Deploying to Vercel...
echo.

vercel --prod --yes

echo.
echo ========================================
echo   Testing deployment...
echo ========================================
echo.

timeout /t 5

curl https://cleanout-pro-bzcz.vercel.app/health

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.

cd ..
pause
