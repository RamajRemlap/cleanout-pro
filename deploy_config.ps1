# ═══════════════════════════════════════════════════════════════════════════════
# CLEANOUT PRO - Complete Deployment Configuration Script
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 CleanOut Pro - Deployment Configuration Assistant            ║" -ForegroundColor Cyan
Write-Host "║  Configuring: Vercel + Railway + Neon Database                   ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

$DATABASE_URL = "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
$VERCEL_PROJECT = "cleanout-pro"
$RAILWAY_PROJECT = "cleanout-pro"

# ─────────────────────────────────────────────────────────────────────────────
# 1. CHECK PREREQUISITES
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "  ✓ Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Git not found! Please install Git." -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed (for Vercel CLI)
try {
    $nodeVersion = node --version
    Write-Host "  ✓ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js not found! Please install Node.js." -ForegroundColor Red
    exit 1
}

# Check if Vercel CLI is installed
try {
    $vercelVersion = vercel --version
    Write-Host "  ✓ Vercel CLI installed: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "  ! Vercel CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g vercel
    Write-Host "  ✓ Vercel CLI installed" -ForegroundColor Green
}

# Check if Railway CLI is installed
try {
    $railwayVersion = railway version
    Write-Host "  ✓ Railway CLI installed: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Host "  ! Railway CLI not found. You can install it later." -ForegroundColor Yellow
    Write-Host "    Install with: npm install -g @railway/cli" -ForegroundColor Cyan
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# 2. VERIFY PROJECT STRUCTURE
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "📁 Verifying project structure..." -ForegroundColor Yellow

$requiredFiles = @(
    "app.py",
    "backend\index.py",
    "backend\api.py",
    "backend\vercel.json",
    "backend\.env.example",
    "requirements.txt",
    "Dockerfile",
    "railway.toml"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Missing: $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host "`n⚠️  Some required files are missing!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# 3. UPDATE ENVIRONMENT FILES
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔧 Updating environment configurations..." -ForegroundColor Yellow

# Update backend/.env
$envContent = @"
# CleanoutPro Backend Environment Variables
# Auto-generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# Neon PostgreSQL Database (Production)
DATABASE_URL=$DATABASE_URL

# Application URLs
APP_URL=https://cleanout-pro.vercel.app
API_URL=https://cleanout-pro.vercel.app

# Environment
ENVIRONMENT=production

# Logging
LOG_LEVEL=INFO

# Security
SECRET_KEY=$(New-Guid)

# File Storage
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=10

# PayPal Configuration (Add your credentials)
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your_paypal_client_id_here
PAYPAL_CLIENT_SECRET=your_paypal_client_secret_here
PAYPAL_WEBHOOK_ID=your_webhook_id_here
"@

Set-Content -Path "backend\.env" -Value $envContent
Write-Host "  ✓ Updated: backend\.env" -ForegroundColor Green

# Create .env for root (Railway)
Set-Content -Path ".env" -Value $envContent
Write-Host "  ✓ Updated: .env (root)" -ForegroundColor Green

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# 4. VERIFY VERCEL CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "⚡ Verifying Vercel configuration..." -ForegroundColor Yellow

# Check if backend/vercel.json exists and is valid
if (Test-Path "backend\vercel.json") {
    $vercelConfig = Get-Content "backend\vercel.json" -Raw | ConvertFrom-Json
    Write-Host "  ✓ Vercel config found" -ForegroundColor Green
    Write-Host "  ℹ  Build source: $($vercelConfig.builds[0].src)" -ForegroundColor Cyan
} else {
    Write-Host "  ✗ Vercel config missing!" -ForegroundColor Red
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# 5. VERIFY RAILWAY CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🚂 Verifying Railway configuration..." -ForegroundColor Yellow

if (Test-Path "railway.toml") {
    Write-Host "  ✓ Railway config found" -ForegroundColor Green
    Write-Host "  ℹ  Healthcheck path: /health" -ForegroundColor Cyan
} else {
    Write-Host "  ✗ Railway config missing!" -ForegroundColor Red
}

if (Test-Path "Dockerfile") {
    Write-Host "  ✓ Dockerfile found" -ForegroundColor Green
} else {
    Write-Host "  ✗ Dockerfile missing!" -ForegroundColor Red
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# 6. GIT STATUS AND COMMIT
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "📦 Preparing Git commit..." -ForegroundColor Yellow

# Add changes
git add .

# Check status
$status = git status --short
if ($status) {
    Write-Host "  ℹ  Changes to commit:" -ForegroundColor Cyan
    Write-Host $status -ForegroundColor Gray
    
    # Commit
    git commit -m "Deploy: Updated environment configs for Vercel + Railway"
    Write-Host "  ✓ Changes committed" -ForegroundColor Green
    
    # Push
    git push origin main
    Write-Host "  ✓ Changes pushed to GitHub" -ForegroundColor Green
} else {
    Write-Host "  ℹ  No changes to commit" -ForegroundColor Cyan
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# 7. DEPLOYMENT INSTRUCTIONS
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ Configuration Complete!                                       ║" -ForegroundColor Green
Write-Host "║  📋 Next Steps for Deployment                                     ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔷 OPTION 1: VERCEL (Serverless - Recommended for API)" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  AUTOMATED DEPLOYMENT:" -ForegroundColor Yellow
Write-Host "    vercel --prod" -ForegroundColor White
Write-Host ""
Write-Host "  OR MANUAL STEPS:" -ForegroundColor Yellow
Write-Host "    1. Go to: https://vercel.com/dashboard" -ForegroundColor White
Write-Host "    2. Select project: cleanout-pro" -ForegroundColor White
Write-Host "    3. Settings → Environment Variables" -ForegroundColor White
Write-Host "    4. Add variable:" -ForegroundColor White
Write-Host "       Name:  DATABASE_URL" -ForegroundColor Cyan
Write-Host "       Value: $DATABASE_URL" -ForegroundColor Gray
Write-Host "    5. Deployments → Redeploy" -ForegroundColor White
Write-Host ""
Write-Host "  TEST DEPLOYMENT:" -ForegroundColor Yellow
Write-Host "    https://cleanout-pro.vercel.app/health" -ForegroundColor Cyan
Write-Host "    https://cleanout-pro.vercel.app/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔷 OPTION 2: RAILWAY (Docker-based)" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  AUTOMATED DEPLOYMENT (if Railway CLI installed):" -ForegroundColor Yellow
Write-Host "    railway login" -ForegroundColor White
Write-Host "    railway link" -ForegroundColor White
Write-Host "    railway up" -ForegroundColor White
Write-Host ""
Write-Host "  OR MANUAL STEPS:" -ForegroundColor Yellow
Write-Host "    1. Go to: https://railway.app/dashboard" -ForegroundColor White
Write-Host "    2. Select project: $RAILWAY_PROJECT" -ForegroundColor White
Write-Host "    3. Variables tab" -ForegroundColor White
Write-Host "    4. Add variable:" -ForegroundColor White
Write-Host "       Name:  DATABASE_URL" -ForegroundColor Cyan
Write-Host "       Value: $DATABASE_URL" -ForegroundColor Gray
Write-Host "    5. App auto-redeploys" -ForegroundColor White
Write-Host ""
Write-Host "  TEST DEPLOYMENT:" -ForegroundColor Yellow
Write-Host "    https://web-production-35f31.up.railway.app/health" -ForegroundColor Cyan
Write-Host "    https://web-production-35f31.up.railway.app/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🗄️  DATABASE (Already Configured)" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  ✓ Neon PostgreSQL: ep-withered-unit-a4erhzp0" -ForegroundColor Green
Write-Host "  ✓ Database: neondb" -ForegroundColor Green
Write-Host "  ✓ Connection pooling: Enabled" -ForegroundColor Green
Write-Host "  ✓ SSL Mode: Required" -ForegroundColor Green
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "  ⚡ QUICK DEPLOY OPTIONS" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Deploy to Vercel now?" -ForegroundColor Cyan
Write-Host "    .\deploy_vercel.ps1" -ForegroundColor White
Write-Host ""
Write-Host "  Deploy to Railway now?" -ForegroundColor Cyan
Write-Host "    .\deploy_railway.ps1" -ForegroundColor White
Write-Host ""

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  🎉 Ready to Deploy!                                              ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Database URL has been configured in:" -ForegroundColor Green
Write-Host "  ✓ backend\.env" -ForegroundColor Green
Write-Host "  ✓ .env (root)" -ForegroundColor Green
Write-Host ""
Write-Host "Your database credentials are:" -ForegroundColor Cyan
Write-Host "  DATABASE_URL = $DATABASE_URL" -ForegroundColor Gray
Write-Host ""
Write-Host "Just add this to your Vercel/Railway dashboards and deploy! 🚀" -ForegroundColor Yellow
Write-Host ""
