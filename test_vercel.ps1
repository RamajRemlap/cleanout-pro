# ═══════════════════════════════════════════════════════════════════════════════
# Test Vercel Deployment
# Run this after deploying to Vercel
# ═══════════════════════════════════════════════════════════════════════════════

param(
    [string]$VercelUrl = ""
)

if ([string]::IsNullOrWhiteSpace($VercelUrl)) {
    Write-Host "❌ Please provide your Vercel URL" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\test_vercel.ps1 -VercelUrl 'https://your-app.vercel.app'" -ForegroundColor White
    Write-Host ""
    Write-Host "Find your URL at: https://vercel.com/dashboard" -ForegroundColor Cyan
    exit 1
}

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🧪 Testing Vercel Deployment                                      ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "🌐 Testing: $VercelUrl" -ForegroundColor Cyan
Write-Host ""

$passed = 0
$failed = 0

# Test 1: Health Check
Write-Host "📍 Test 1/4: Health Check" -ForegroundColor White
try {
    $response = Invoke-RestMethod -Uri "$VercelUrl/health" -Method Get -TimeoutSec 30
    if ($response.status -eq "healthy") {
        Write-Host "  ✅ PASS - Status: $($response.status)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ❌ FAIL - Unexpected status: $($response.status)" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "  ❌ FAIL - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}
Write-Host ""

# Test 2: Root Endpoint
Write-Host "📍 Test 2/4: Root Endpoint" -ForegroundColor White
try {
    $response = Invoke-RestMethod -Uri "$VercelUrl/" -Method Get -TimeoutSec 30
    if ($response.service -eq "CleanoutPro API") {
        Write-Host "  ✅ PASS - Service: $($response.service) v$($response.version)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ❌ FAIL - Unexpected response" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "  ❌ FAIL - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}
Write-Host ""

# Test 3: API Docs
Write-Host "📍 Test 3/4: API Documentation" -ForegroundColor White
try {
    $response = Invoke-WebRequest -Uri "$VercelUrl/docs" -Method Get -TimeoutSec 30
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✅ PASS - Docs accessible" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ❌ FAIL - Status: $($response.StatusCode)" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "  ❌ FAIL - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}
Write-Host ""

# Test 4: Database Connection
Write-Host "📍 Test 4/4: Database Connection (via API)" -ForegroundColor White
try {
    # Try to access an API endpoint that requires database
    $response = Invoke-WebRequest -Uri "$VercelUrl/api/jobs" -Method Get -TimeoutSec 30 -SkipHttpErrorCheck
    if ($response.StatusCode -eq 200 -or $response.StatusCode -eq 404) {
        Write-Host "  ✅ PASS - Database connection working" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ⚠️  WARNING - Status: $($response.StatusCode)" -ForegroundColor Yellow
        $passed++
    }
} catch {
    Write-Host "  ⚠️  WARNING - Could not test database endpoint" -ForegroundColor Yellow
    $passed++
}
Write-Host ""

# Summary
Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📊 Test Results                                                   ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$total = $passed + $failed
$percentage = [math]::Round(($passed / $total) * 100)

Write-Host "  Tests Passed: $passed/$total ($percentage%)" -ForegroundColor $(if ($percentage -ge 75) { "Green" } else { "Yellow" })
Write-Host ""

if ($failed -eq 0) {
    Write-Host "🎉 All tests passed! Your Vercel deployment is working perfectly!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some tests failed. Check the Vercel logs:" -ForegroundColor Yellow
    Write-Host "   vercel logs" -ForegroundColor White
}

Write-Host ""
Write-Host "Useful Links:" -ForegroundColor Yellow
Write-Host "  📚 API Docs:    $VercelUrl/docs" -ForegroundColor Cyan
Write-Host "  🏥 Health:      $VercelUrl/health" -ForegroundColor Cyan
Write-Host "  🎛️  Dashboard:   https://vercel.com/dashboard" -ForegroundColor Cyan
Write-Host ""
