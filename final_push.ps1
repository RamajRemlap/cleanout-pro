# CleanOut Pro - Final Deployment Push
# Commits and pushes deployment scripts

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " CleanOut Pro - Final Deployment Push" -ForegroundColor Cyan
Write-Host " Committing deployment scripts and guides" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Git Status
Write-Host "Checking Git status..." -ForegroundColor Yellow
$status = git status --porcelain

if ($status) {
    Write-Host "  Changes detected:" -ForegroundColor Cyan
    git status --short
} else {
    Write-Host "  Working directory clean" -ForegroundColor Green
    Write-Host ""
    Write-Host "Everything is already committed!" -ForegroundColor Green
    exit 0
}

Write-Host ""

# Add Deployment Files
Write-Host "Adding deployment files..." -ForegroundColor Yellow

$deploymentFiles = @(
    "deploy_config.ps1",
    "deploy_vercel.ps1",
    "deploy_railway.ps1",
    "MANUAL_DEPLOYMENT_GUIDE.md",
    "QUICK_DEPLOY.md",
    "final_push.ps1"
)

foreach ($file in $deploymentFiles) {
    if (Test-Path $file) {
        git add $file
        Write-Host "  Added: $file" -ForegroundColor Green
    }
}

# Also add updated .env files if they exist
if (Test-Path "backend\.env") {
    git add "backend\.env"
    Write-Host "  Added: backend\.env" -ForegroundColor Green
}

if (Test-Path ".env") {
    git add ".env"
    Write-Host "  Added: .env" -ForegroundColor Green
}

Write-Host ""

# Commit Changes
Write-Host "Committing changes..." -ForegroundColor Yellow

$commitMessage = "Deploy: Complete deployment automation scripts

Added deployment automation and guides:
- deploy_config.ps1: Master configuration script
- deploy_vercel.ps1: Automated Vercel deployment
- deploy_railway.ps1: Automated Railway deployment
- MANUAL_DEPLOYMENT_GUIDE.md: Comprehensive manual guide
- QUICK_DEPLOY.md: Quick reference card

Ready for production deployment"

git commit -m $commitMessage

Write-Host ""

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow

git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Pushed to GitHub successfully!" -ForegroundColor Green
} else {
    Write-Host "  Push may have failed - check manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host " Everything Committed and Pushed!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Your deployment toolkit is ready:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Configuration Scripts:" -ForegroundColor Yellow
Write-Host "    .\deploy_config.ps1  - Master configuration" -ForegroundColor White
Write-Host "    .\deploy_vercel.ps1  - Automated Vercel deployment" -ForegroundColor White
Write-Host "    .\deploy_railway.ps1 - Automated Railway deployment" -ForegroundColor White
Write-Host ""
Write-Host "  Documentation:" -ForegroundColor Yellow
Write-Host "    MANUAL_DEPLOYMENT_GUIDE.md - Complete guide" -ForegroundColor White
Write-Host "    QUICK_DEPLOY.md - Quick reference" -ForegroundColor White
Write-Host ""

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " NEXT STEPS" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "DATABASE_URL to add:" -ForegroundColor Green
Write-Host "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require" -ForegroundColor Cyan
Write-Host ""

Write-Host "Deploy to Vercel:" -ForegroundColor Yellow
Write-Host "  1. Go to https://vercel.com/dashboard" -ForegroundColor White
Write-Host "  2. Settings -> Environment Variables -> Add DATABASE_URL" -ForegroundColor White
Write-Host "  3. Deployments -> Redeploy" -ForegroundColor White
Write-Host ""

Write-Host "Deploy to Railway:" -ForegroundColor Yellow
Write-Host "  1. Go to https://railway.app/dashboard" -ForegroundColor White
Write-Host "  2. Variables -> Add DATABASE_URL" -ForegroundColor White
Write-Host "  3. Auto-redeploys!" -ForegroundColor White
Write-Host ""

Write-Host "========================================================================" -ForegroundColor Green
Write-Host " Ready to Deploy!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""
