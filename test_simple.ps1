# Simple deployment test script
param(
    [string]$VercelUrl = "",
    [string]$RailwayUrl = "https://web-production-35f31.up.railway.app"
)

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🧪 CleanOut Pro - Deployment Tests                               ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$totalTests = 0
$totalPassed = 0
$totalFailed = 0

# Test Railway
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  Testing Railway Deployment                                        ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Base URL: $RailwayUrl" -ForegroundColor Cyan
Write-Host ""

# Test 1: Root endpoint
Write-Host "📍 Test 1/4: Root Endpoint" -ForegroundColor White
Write-Host "  Testing: $RailwayUrl/" -ForegroundColor Cyan
$totalTests++

try {
    $response = Invoke-RestMethod -Uri "$RailwayUrl/" -Method Get -ErrorAction Stop -TimeoutSec 30
    Write-Host "    ✓ Status: 200 OK" -ForegroundColor Green
    Write-Host "    ✓ Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
    $totalPassed++
}
catch {
    Write-Host "    ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    $totalFailed++
}
Write-Host ""

# Test 2: Health check
Write-Host "📍 Test 2/4: Health Check" -ForegroundColor White
Write-Host "  Testing: $RailwayUrl/health" -ForegroundColor Cyan
$totalTests++

try {
    $response = Invoke-RestMethod -Uri "$RailwayUrl/health" -Method Get -ErrorAction Stop -TimeoutSec 30
    Write-Host "    ✓ Status: 200 OK" -ForegroundColor Green
    Write-Host "    ✓ Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
    $totalPassed++
}
catch {
    Write-Host "    ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    $totalFailed++
}
Write-Host ""

# Test 3: API docs
Write-Host "📍 Test 3/4: API Documentation" -ForegroundColor White
Write-Host "  Testing: $RailwayUrl/docs" -ForegroundColor Cyan
$totalTests++

try {
    $response = Invoke-WebRequest -Uri "$RailwayUrl/docs" -Method Get -ErrorAction Stop -TimeoutSec 30
    if ($response.StatusCode -eq 200) {
        Write-Host "    ✓ Status: 200 OK" -ForegroundColor Green
        $totalPassed++
    }
    else {
        Write-Host "    ⚠ Status: $($response.StatusCode)" -ForegroundColor Yellow
        $totalFailed++
    }
}
catch {
    Write-Host "    ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    $totalFailed++
}
Write-Host ""

# Test 4: ReDoc
Write-Host "📍 Test 4/4: ReDoc Documentation" -ForegroundColor White
Write-Host "  Testing: $RailwayUrl/redoc" -ForegroundColor Cyan
$totalTests++

try {
    $response = Invoke-WebRequest -Uri "$RailwayUrl/redoc" -Method Get -ErrorAction Stop -TimeoutSec 30
    if ($response.StatusCode -eq 200) {
        Write-Host "    ✓ Status: 200 OK" -ForegroundColor Green
        $totalPassed++
    }
    else {
        Write-Host "    ⚠ Status: $($response.StatusCode)" -ForegroundColor Yellow
        $totalFailed++
    }
}
catch {
    Write-Host "    ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    $totalFailed++
}
Write-Host ""

# Summary
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

if ($totalFailed -eq 0) {
    Write-Host "  ✅ All tests passed! ($totalPassed/$totalTests)" -ForegroundColor Green
}
elseif ($totalPassed -eq 0) {
    Write-Host "  ❌ All tests failed! ($totalFailed/$totalTests)" -ForegroundColor Red
}
else {
    Write-Host "  ⚠️  Partial success: $totalPassed/$totalTests passed, $totalFailed failed" -ForegroundColor Yellow
}
Write-Host ""

# Overall Summary
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📊 Overall Summary                                                ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

if ($totalFailed -eq 0) {
    Write-Host "  🎉 Railway deployment is working perfectly!" -ForegroundColor Green
    Write-Host "  Total: $totalPassed/$totalTests tests passed" -ForegroundColor Green
}
else {
    Write-Host "  📊 Results: $totalPassed passed, $totalFailed failed (out of $totalTests total)" -ForegroundColor Yellow
}

Write-Host ""

# Troubleshooting if needed
if ($totalFailed -gt 0) {
    Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║  🔧 Troubleshooting                                                ║" -ForegroundColor Yellow
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "If tests failed, check:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. Environment Variables" -ForegroundColor White
    Write-Host "     - Railway: Variables tab → DATABASE_URL" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Deployment Status" -ForegroundColor White
    Write-Host "     - Railway: Run 'railway logs' or check dashboard" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. Build Errors" -ForegroundColor White
    Write-Host "     - Check build logs for Python import errors" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📚 Useful Links                                                   ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "Railway:" -ForegroundColor Yellow
Write-Host "  🌐 App:       $RailwayUrl" -ForegroundColor White
Write-Host "  📚 Docs:      $RailwayUrl/docs" -ForegroundColor White
Write-Host "  🏥 Health:    $RailwayUrl/health" -ForegroundColor White
Write-Host "  🎛️  Dashboard: https://railway.app/dashboard" -ForegroundColor Cyan
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
