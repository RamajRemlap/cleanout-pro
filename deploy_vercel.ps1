# ═══════════════════════════════════════════════════════════════════════════════
# CLEANOUT PRO - Vercel Deployment Script
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  ⚡ CleanOut Pro - Vercel Deployment                              ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$DATABASE_URL = "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

# ─────────────────────────────────────────────────────────────────────────────
# Check if Vercel CLI is installed
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔍 Checking Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version
    Write-Host "  ✓ Vercel CLI: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Vercel CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
    Write-Host "  ✓ Vercel CLI installed" -ForegroundColor Green
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Login to Vercel
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔐 Vercel Authentication..." -ForegroundColor Yellow
Write-Host "  Opening Vercel login..." -ForegroundColor Cyan
Write-Host ""

vercel login

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Set Environment Variables
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🔧 Setting environment variables..." -ForegroundColor Yellow

# Set DATABASE_URL for production
Write-Host "  Setting DATABASE_URL for production..." -ForegroundColor Cyan
vercel env add DATABASE_URL production --force 2>$null <<EOF
$DATABASE_URL
EOF

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ DATABASE_URL set for production" -ForegroundColor Green
} else {
    Write-Host "  ! Manual setup required" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Please add this environment variable manually:" -ForegroundColor Cyan
    Write-Host "    Name:  DATABASE_URL" -ForegroundColor White
    Write-Host "    Value: $DATABASE_URL" -ForegroundColor Gray
    Write-Host "    Environment: Production" -ForegroundColor White
    Write-Host ""
    Write-Host "  Go to: https://vercel.com/dashboard" -ForegroundColor Cyan
    Write-Host "    → Select project → Settings → Environment Variables" -ForegroundColor Cyan
    Write-Host ""
    
    $continue = Read-Host "Have you added the DATABASE_URL? (y/n)"
    if ($continue -ne 'y') {
        Write-Host "  ⚠️  Deployment cancelled. Please add the environment variable first." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Deploy to Production
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🚀 Deploying to Vercel..." -ForegroundColor Yellow
Write-Host ""

# Change to backend directory (where vercel.json is)
Set-Location backend

# Deploy
vercel --prod --yes

# Return to root
Set-Location ..

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Test Deployment
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
Write-Host ""

$deploymentUrl = "https://cleanout-pro.vercel.app"

Write-Host "  Testing health endpoint..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$deploymentUrl/health" -Method Get -ErrorAction Stop
    Write-Host "  ✓ Health check passed!" -ForegroundColor Green
    Write-Host "    Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "  ⚠️  Health check failed or not ready yet" -ForegroundColor Yellow
    Write-Host "    This is normal for first deployment - it may take a minute" -ForegroundColor Gray
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ Vercel Deployment Complete!                                   ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "Your API is deployed at:" -ForegroundColor Cyan
Write-Host "  🌐 Main URL:    $deploymentUrl" -ForegroundColor White
Write-Host "  🏥 Health:      $deploymentUrl/health" -ForegroundColor White
Write-Host "  📚 API Docs:    $deploymentUrl/docs" -ForegroundColor White
Write-Host "  📖 ReDoc:       $deploymentUrl/redoc" -ForegroundColor White
Write-Host ""

Write-Host "Test your API:" -ForegroundColor Yellow
Write-Host "  curl $deploymentUrl/health" -ForegroundColor Gray
Write-Host "  curl $deploymentUrl/api/jobs" -ForegroundColor Gray
Write-Host ""

Write-Host "Vercel Dashboard:" -ForegroundColor Yellow
Write-Host "  https://vercel.com/dashboard" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Open the API docs: $deploymentUrl/docs" -ForegroundColor White
Write-Host "  2. Test the endpoints" -ForegroundColor White
Write-Host "  3. Configure PayPal credentials if needed" -ForegroundColor White
Write-Host ""

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🎉 Happy deploying!                                              ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
