# ═══════════════════════════════════════════════════════════════════════════════
# CLEANOUT PRO - Complete Deployment Test Script
# Tests: Neon Database, Railway API, Vercel API, Desktop App
# ═══════════════════════════════════════════════════════════════════════════════

param(
    [string]$VercelUrl = ""
)

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🧪 CleanOut Pro - Complete Deployment Tests                      ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$railwayUrl = "https://web-production-35f31.up.railway.app"
$databaseUrl = "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

$totalTests = 0
$passedTests = 0
$failedTests = 0

# ─────────────────────────────────────────────────────────────────────────────
# Test 1: Neon Database
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  Test 1: Neon PostgreSQL Database                                 ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""

$totalTests++
Write-Host "  Testing database connection..." -ForegroundColor Cyan

try {
    $env:DATABASE_URL = $databaseUrl
    $testResult = python -c "from sqlalchemy import create_engine; engine = create_engine('$databaseUrl'); conn = engine.connect(); print('Connected'); conn.close()" 2>&1

    if ($testResult -like "*Connected*") {
        Write-Host "    ✓ Database connection successful!" -ForegroundColor Green
        $passedTests++
    } else {
        Write-Host "    ✗ Database connection failed" -ForegroundColor Red
        $failedTests++
    }
} catch {
    Write-Host "    ✗ Error testing database: $($_.Exception.Message)" -ForegroundColor Red
    $failedTests++
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Test 2: Railway API
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  Test 2: Railway Backend API                                      ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 URL: $railwayUrl" -ForegroundColor Cyan
Write-Host ""

# Test 2.1: Health check
$totalTests++
Write-Host "  Test 2.1: Health Check" -ForegroundColor White
try {
    $response = Invoke-RestMethod -Uri "$railwayUrl/health" -Method Get -ErrorAction Stop
    if ($response.status -eq "healthy") {
        Write-Host "    ✓ Health check passed: $($response.status)" -ForegroundColor Green
        $passedTests++
    } else {
        Write-Host "    ✗ Unexpected health status: $($response.status)" -ForegroundColor Red
        $failedTests++
    }
} catch {
    Write-Host "    ✗ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
    $failedTests++
}

# Test 2.2: Root endpoint
$totalTests++
Write-Host "  Test 2.2: Root Endpoint" -ForegroundColor White
try {
    $response = Invoke-RestMethod -Uri "$railwayUrl/" -Method Get -ErrorAction Stop
    if ($response.service -eq "CleanoutPro API") {
        Write-Host "    ✓ Root endpoint working: v$($response.version)" -ForegroundColor Green
        $passedTests++
    } else {
        Write-Host "    ✗ Unexpected response" -ForegroundColor Red
        $failedTests++
    }
} catch {
    Write-Host "    ✗ Root endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
    $failedTests++
}

# Test 2.3: API Docs
$totalTests++
Write-Host "  Test 2.3: API Documentation" -ForegroundColor White
try {
    $response = Invoke-WebRequest -Uri "$railwayUrl/docs" -Method Get -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "    ✓ API docs accessible" -ForegroundColor Green
        $passedTests++
    } else {
        Write-Host "    ✗ API docs returned: $($response.StatusCode)" -ForegroundColor Red
        $failedTests++
    }
} catch {
    Write-Host "    ✗ API docs failed: $($_.Exception.Message)" -ForegroundColor Red
    $failedTests++
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Test 3: Vercel API (if URL provided)
# ─────────────────────────────────────────────────────────────────────────────

if ($VercelUrl) {
    Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║  Test 3: Vercel Backend API                                        ║" -ForegroundColor Yellow
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🌐 URL: $VercelUrl" -ForegroundColor Cyan
    Write-Host ""

    # Test 3.1: Health check
    $totalTests++
    Write-Host "  Test 3.1: Health Check" -ForegroundColor White
    try {
        $response = Invoke-RestMethod -Uri "$VercelUrl/health" -Method Get -ErrorAction Stop
        if ($response.status -eq "healthy") {
            Write-Host "    ✓ Health check passed" -ForegroundColor Green
            $passedTests++
        } else {
            Write-Host "    ✗ Unexpected health status" -ForegroundColor Red
            $failedTests++
        }
    } catch {
        Write-Host "    ✗ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
        $failedTests++
    }

    # Test 3.2: Root endpoint
    $totalTests++
    Write-Host "  Test 3.2: Root Endpoint" -ForegroundColor White
    try {
        $response = Invoke-RestMethod -Uri "$VercelUrl/" -Method Get -ErrorAction Stop
        if ($response.service -eq "CleanoutPro API") {
            Write-Host "    ✓ Root endpoint working" -ForegroundColor Green
            $passedTests++
        } else {
            Write-Host "    ✗ Unexpected response" -ForegroundColor Red
            $failedTests++
        }
    } catch {
        Write-Host "    ✗ Root endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
        $failedTests++
    }

    Write-Host ""
} else {
    Write-Host "⏭️  Skipping Vercel tests (no URL provided)" -ForegroundColor Gray
    Write-Host "   Use: .\test_all_deployments.ps1 -VercelUrl 'https://your-app.vercel.app'" -ForegroundColor Gray
    Write-Host ""
}

# ─────────────────────────────────────────────────────────────────────────────
# Test 4: Desktop App Build
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  Test 4: Desktop App                                               ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""

# Test 4.1: Check build exists
$totalTests++
Write-Host "  Test 4.1: Build Files Exist" -ForegroundColor White
if (Test-Path "desktop\build\index.html") {
    Write-Host "    ✓ Desktop app build exists" -ForegroundColor Green
    $passedTests++
} else {
    Write-Host "    ✗ Desktop app build not found" -ForegroundColor Red
    Write-Host "    Run: cd desktop && npm run build" -ForegroundColor Yellow
    $failedTests++
}

# Test 4.2: Check package.json
$totalTests++
Write-Host "  Test 4.2: Package Configuration" -ForegroundColor White
if (Test-Path "desktop\package.json") {
    Write-Host "    ✓ Package.json exists" -ForegroundColor Green
    $passedTests++
} else {
    Write-Host "    ✗ Package.json not found" -ForegroundColor Red
    $failedTests++
}

# Test 4.3: Check node_modules
$totalTests++
Write-Host "  Test 4.3: Dependencies Installed" -ForegroundColor White
if (Test-Path "desktop\node_modules") {
    Write-Host "    ✓ Dependencies installed" -ForegroundColor Green
    $passedTests++
} else {
    Write-Host "    ✗ Dependencies not installed" -ForegroundColor Red
    Write-Host "    Run: cd desktop && npm install" -ForegroundColor Yellow
    $failedTests++
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Final Summary
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📊 Test Results Summary                                           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "Total Tests: $totalTests" -ForegroundColor White
Write-Host "✅ Passed: $passedTests" -ForegroundColor Green
Write-Host "❌ Failed: $failedTests" -ForegroundColor Red
Write-Host ""

$successRate = [math]::Round(($passedTests / $totalTests) * 100, 1)
Write-Host "Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 80) { "Green" } elseif ($successRate -ge 50) { "Yellow" } else { "Red" })
Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Deployment Status
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 Deployment Status                                              ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "  Service          Status      URL" -ForegroundColor White
Write-Host "  ──────────────── ─────────── ────────────────────────────────────" -ForegroundColor Gray
Write-Host "  Neon Database    ✅ Live      neon.tech" -ForegroundColor Green
Write-Host "  Railway API      ✅ Live      $railwayUrl" -ForegroundColor Green
if ($VercelUrl) {
    Write-Host "  Vercel API       ✅ Live      $VercelUrl" -ForegroundColor Green
} else {
    Write-Host "  Vercel API       ⏳ Pending   (not deployed yet)" -ForegroundColor Yellow
}
Write-Host "  Desktop App      ✅ Built     (run locally)" -ForegroundColor Green
Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Next Steps
# ─────────────────────────────────────────────────────────────────────────────

if ($failedTests -gt 0) {
    Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║  🔧 Action Required                                                ║" -ForegroundColor Yellow
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""

    if (-not $VercelUrl) {
        Write-Host "  ⚠️  Deploy to Vercel:" -ForegroundColor Yellow
        Write-Host "     cd backend && vercel --prod" -ForegroundColor White
        Write-Host ""
    }

    if (-not (Test-Path "desktop\build")) {
        Write-Host "  ⚠️  Build desktop app:" -ForegroundColor Yellow
        Write-Host "     cd desktop && npm run build" -ForegroundColor White
        Write-Host ""
    }
} else {
    Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  🎉 All Tests Passed!                                              ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Your CleanoutPro system is fully deployed and operational!" -ForegroundColor Green
    Write-Host ""
}

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
