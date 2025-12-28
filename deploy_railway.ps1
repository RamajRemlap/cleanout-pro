# ═══════════════════════════════════════════════════════════════════════════════
# CLEANOUT PRO - Railway Deployment Script
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚂 CleanOut Pro - Railway Deployment                             ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$DATABASE_URL = "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

# ─────────────────────────────────────────────────────────────────────────────
# Check if Railway CLI is installed
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔍 Checking Railway CLI..." -ForegroundColor Yellow
try {
    $railwayVersion = railway version
    Write-Host "  ✓ Railway CLI: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Railway CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing Railway CLI..." -ForegroundColor Yellow
    npm install -g @railway/cli
    Write-Host "  ✓ Railway CLI installed" -ForegroundColor Green
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Login to Railway
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔐 Railway Authentication..." -ForegroundColor Yellow
Write-Host "  Opening Railway login..." -ForegroundColor Cyan
Write-Host ""

railway login

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Link to Project
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔗 Linking to Railway project..." -ForegroundColor Yellow

# Check if already linked
if (Test-Path ".railway") {
    Write-Host "  ℹ  Already linked to a Railway project" -ForegroundColor Cyan
} else {
    Write-Host "  Please select your project..." -ForegroundColor Cyan
    railway link
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Set Environment Variables
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔧 Setting environment variables..." -ForegroundColor Yellow

# Set DATABASE_URL
Write-Host "  Setting DATABASE_URL..." -ForegroundColor Cyan
railway variables set DATABASE_URL="$DATABASE_URL" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ DATABASE_URL set" -ForegroundColor Green
} else {
    Write-Host "  ! Manual setup required" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Please add this environment variable manually:" -ForegroundColor Cyan
    Write-Host "    Name:  DATABASE_URL" -ForegroundColor White
    Write-Host "    Value: $DATABASE_URL" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Go to: https://railway.app/dashboard" -ForegroundColor Cyan
    Write-Host "    → Select project → Variables tab" -ForegroundColor Cyan
    Write-Host ""
    
    $continue = Read-Host "Have you added the DATABASE_URL? (y/n)"
    if ($continue -ne 'y') {
        Write-Host "  ⚠️  Deployment cancelled. Please add the environment variable first." -ForegroundColor Red
        exit 1
    }
}

# Set other environment variables
Write-Host "  Setting ENVIRONMENT=production..." -ForegroundColor Cyan
railway variables set ENVIRONMENT="production" 2>$null

Write-Host "  Setting LOG_LEVEL=INFO..." -ForegroundColor Cyan
railway variables set LOG_LEVEL="INFO" 2>$null

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Deploy
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🚀 Deploying to Railway..." -ForegroundColor Yellow
Write-Host ""

# Deploy using Railway CLI
railway up

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Get Deployment URL
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "📋 Getting deployment info..." -ForegroundColor Yellow

try {
    $deploymentInfo = railway status
    Write-Host $deploymentInfo -ForegroundColor Gray
} catch {
    Write-Host "  ℹ  Run 'railway status' to see deployment details" -ForegroundColor Cyan
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Test Deployment
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
Write-Host ""

$deploymentUrl = "https://web-production-35f31.up.railway.app"

Write-Host "  Testing health endpoint..." -ForegroundColor Cyan
Write-Host "  URL: $deploymentUrl/health" -ForegroundColor Gray

Start-Sleep -Seconds 5  # Wait for deployment

try {
    $response = Invoke-RestMethod -Uri "$deploymentUrl/health" -Method Get -ErrorAction Stop
    Write-Host "  ✓ Health check passed!" -ForegroundColor Green
    Write-Host "    Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "  ⚠️  Health check failed or not ready yet" -ForegroundColor Yellow
    Write-Host "    This is normal for first deployment - it may take a few minutes" -ForegroundColor Gray
    Write-Host "    Check Railway logs: railway logs" -ForegroundColor Cyan
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ Railway Deployment Complete!                                  ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "Your API is deployed at:" -ForegroundColor Cyan
Write-Host "  🌐 Main URL:    $deploymentUrl" -ForegroundColor White
Write-Host "  🏥 Health:      $deploymentUrl/health" -ForegroundColor White
Write-Host "  📚 API Docs:    $deploymentUrl/docs" -ForegroundColor White
Write-Host "  📖 ReDoc:       $deploymentUrl/redoc" -ForegroundColor White
Write-Host ""

Write-Host "Useful Railway Commands:" -ForegroundColor Yellow
Write-Host "  railway logs              # View logs" -ForegroundColor Gray
Write-Host "  railway status            # Check status" -ForegroundColor Gray
Write-Host "  railway variables         # List variables" -ForegroundColor Gray
Write-Host "  railway open              # Open in browser" -ForegroundColor Gray
Write-Host ""

Write-Host "Railway Dashboard:" -ForegroundColor Yellow
Write-Host "  https://railway.app/dashboard" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Check logs: railway logs" -ForegroundColor White
Write-Host "  2. Open the API docs: $deploymentUrl/docs" -ForegroundColor White
Write-Host "  3. Test the endpoints" -ForegroundColor White
Write-Host ""

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🎉 Happy deploying!                                              ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
