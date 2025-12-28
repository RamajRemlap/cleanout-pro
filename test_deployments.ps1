# ═══════════════════════════════════════════════════════════════════════════════
# CLEANOUT PRO - Deployment Test Script
# Tests both Vercel and Railway deployments
# ═══════════════════════════════════════════════════════════════════════════════

param(
    [string]$VercelUrl = "",
    [string]$RailwayUrl = "https://web-production-35f31.up.railway.app"
)

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🧪 CleanOut Pro - Deployment Tests                               ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url
    )

    Write-Host "  Testing: $Url" -ForegroundColor Cyan

    try {
        $response = Invoke-WebRequest -Uri $Url -Method Get -ErrorAction Stop -TimeoutSec 30

        if ($response.StatusCode -eq 200) {
            Write-Host "    ✓ Status: $($response.StatusCode) OK" -ForegroundColor Green

            # Try to parse JSON response
            try {
                $json = $response.Content | ConvertFrom-Json
                Write-Host "    ✓ Response: $($json | ConvertTo-Json -Compress)" -ForegroundColor Gray
                return $true
            }
            catch {
                Write-Host "    ✓ Response received (non-JSON)" -ForegroundColor Gray
                return $true
            }
        }
        else {
            Write-Host "    ⚠ Status: $($response.StatusCode)" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.Value__
        if ($statusCode) {
            Write-Host "    ✗ Status: $statusCode - $($_.Exception.Message)" -ForegroundColor Red
        }
        else {
            Write-Host "    ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
        }
        Write-Host "    ℹ  Possible causes:" -ForegroundColor Yellow
        Write-Host "      - Deployment still in progress" -ForegroundColor Gray
        Write-Host "      - Environment variables not set" -ForegroundColor Gray
        Write-Host "      - Build failed" -ForegroundColor Gray
        return $false
    }
}

function Test-Deployment {
    param(
        [string]$Platform,
        [string]$BaseUrl
    )

    Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║  Testing $Platform Deployment" -ForegroundColor Yellow
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""

    if ([string]::IsNullOrWhiteSpace($BaseUrl)) {
        Write-Host "  ⚠️  No URL provided for $Platform" -ForegroundColor Yellow
        Write-Host "  Skipping $Platform tests" -ForegroundColor Gray
        Write-Host ""
        return @{
            Platform = $Platform
            Status = "Skipped"
            Passed = 0
            Failed = 0
            Total = 0
        }
    }

    Write-Host "🌐 Base URL: $BaseUrl" -ForegroundColor Cyan
    Write-Host ""

    $results = @{
        Platform = $Platform
        BaseUrl = $BaseUrl
        Passed = 0
        Failed = 0
        Total = 0
    }

    # Test 1: Root endpoint
    Write-Host "📍 Test 1/4: Root Endpoint" -ForegroundColor White
    $results.Total++
    if (Test-Endpoint -Name "Root" -Url "$BaseUrl/") {
        $results.Passed++
    }
    else {
        $results.Failed++
    }
    Write-Host ""

    # Test 2: Health check
    Write-Host "📍 Test 2/4: Health Check" -ForegroundColor White
    $results.Total++
    if (Test-Endpoint -Name "Health" -Url "$BaseUrl/health") {
        $results.Passed++
    }
    else {
        $results.Failed++
    }
    Write-Host ""

    # Test 3: API docs
    Write-Host "📍 Test 3/4: API Documentation" -ForegroundColor White
    $results.Total++
    if (Test-Endpoint -Name "Docs" -Url "$BaseUrl/docs") {
        $results.Passed++
    }
    else {
        $results.Failed++
    }
    Write-Host ""

    # Test 4: ReDoc
    Write-Host "📍 Test 4/4: ReDoc Documentation" -ForegroundColor White
    $results.Total++
    if (Test-Endpoint -Name "ReDoc" -Url "$BaseUrl/redoc") {
        $results.Passed++
    }
    else {
        $results.Failed++
    }
    Write-Host ""

    # Summary for this platform
    Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
    if ($results.Failed -eq 0) {
        Write-Host "  ✅ All tests passed! ($($results.Passed)/$($results.Total))" -ForegroundColor Green
        $results.Status = "Success"
    }
    elseif ($results.Passed -eq 0) {
        Write-Host "  ❌ All tests failed! ($($results.Failed)/$($results.Total))" -ForegroundColor Red
        $results.Status = "Failed"
    }
    else {
        Write-Host "  ⚠️  Partial success: $($results.Passed)/$($results.Total) passed, $($results.Failed) failed" -ForegroundColor Yellow
        $results.Status = "Partial"
    }
    Write-Host ""

    return $results
}

# ─────────────────────────────────────────────────────────────────────────────
# Get Vercel URL if not provided
# ─────────────────────────────────────────────────────────────────────────────

if ([string]::IsNullOrWhiteSpace($VercelUrl)) {
    Write-Host "🔍 No Vercel URL provided. Attempting to detect..." -ForegroundColor Yellow

    try {
        # Try to get Vercel URL from CLI
        $vercelInfo = vercel ls 2>&1 | Select-String -Pattern "https://" | Select-Object -First 1
        if ($vercelInfo) {
            $VercelUrl = ($vercelInfo -replace '\s+', ' ' -split ' ' | Where-Object { $_ -like "https://*" })[0]
            Write-Host "  ✓ Detected Vercel URL: $VercelUrl" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "  ℹ️  Could not auto-detect Vercel URL" -ForegroundColor Cyan
        Write-Host "  You can provide it manually:" -ForegroundColor Cyan
        Write-Host "    .\test_deployments.ps1 -VercelUrl 'https://your-app.vercel.app'" -ForegroundColor Gray
    }
    Write-Host ""
}

# ─────────────────────────────────────────────────────────────────────────────
# Run Tests
# ─────────────────────────────────────────────────────────────────────────────

$allResults = @()

# Test Vercel
if (-not [string]::IsNullOrWhiteSpace($VercelUrl)) {
    $vercelResults = Test-Deployment -Platform "Vercel" -BaseUrl $VercelUrl
    $allResults += $vercelResults
    Start-Sleep -Seconds 2
}
else {
    Write-Host "⏭️  Skipping Vercel tests (no URL provided)" -ForegroundColor Gray
    Write-Host ""
}

# Test Railway
$railwayResults = Test-Deployment -Platform "Railway" -BaseUrl $RailwayUrl
$allResults += $railwayResults

# ─────────────────────────────────────────────────────────────────────────────
# Final Summary
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📊 Overall Summary                                                ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$totalPassed = ($allResults | Measure-Object -Property Passed -Sum).Sum
$totalFailed = ($allResults | Measure-Object -Property Failed -Sum).Sum
$totalTests = ($allResults | Measure-Object -Property Total -Sum).Sum

foreach ($result in $allResults) {
    $statusColor = switch ($result.Status) {
        "Success" { "Green" }
        "Failed" { "Red" }
        "Partial" { "Yellow" }
        "Skipped" { "Gray" }
        default { "White" }
    }

    $statusIcon = switch ($result.Status) {
        "Success" { "✅" }
        "Failed" { "❌" }
        "Partial" { "⚠️ " }
        "Skipped" { "⏭️ " }
        default { "•" }
    }

    Write-Host "  $statusIcon $($result.Platform): " -NoNewline -ForegroundColor $statusColor
    if ($result.Status -eq "Skipped") {
        Write-Host "Skipped" -ForegroundColor Gray
    }
    else {
        Write-Host "$($result.Passed)/$($result.Total) passed" -ForegroundColor $statusColor
        if ($result.BaseUrl) {
            Write-Host "     URL: $($result.BaseUrl)" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

if ($totalTests -eq 0) {
    Write-Host "  ⚠️  No tests were run" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Usage:" -ForegroundColor Cyan
    Write-Host "    .\test_deployments.ps1 -VercelUrl 'https://your-app.vercel.app'" -ForegroundColor Gray
}
elseif ($totalFailed -eq 0) {
    Write-Host "  🎉 All deployments are working perfectly!" -ForegroundColor Green
    Write-Host "  Total: $totalPassed/$totalTests tests passed" -ForegroundColor Green
}
else {
    Write-Host "  📊 Results: $totalPassed passed, $totalFailed failed (out of $totalTests total)" -ForegroundColor Yellow
}

Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# Next Steps
# ─────────────────────────────────────────────────────────────────────────────

if ($totalFailed -gt 0) {
    Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║  🔧 Troubleshooting                                                ║" -ForegroundColor Yellow
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "If tests failed, check:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. Environment Variables" -ForegroundColor White
    Write-Host "     - Vercel: Settings → Environment Variables → DATABASE_URL" -ForegroundColor Gray
    Write-Host "     - Railway: Variables tab → DATABASE_URL" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Deployment Status" -ForegroundColor White
    Write-Host "     - Vercel: Check deployment logs at https://vercel.com/dashboard" -ForegroundColor Gray
    Write-Host "     - Railway: Run 'railway logs' or check dashboard" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. Build Errors" -ForegroundColor White
    Write-Host "     - Check build logs for Python import errors" -ForegroundColor Gray
    Write-Host "     - Verify requirements.txt is complete" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📚 Useful Links                                                   ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

if (-not [string]::IsNullOrWhiteSpace($VercelUrl)) {
    Write-Host "Vercel:" -ForegroundColor Yellow
    Write-Host "  🌐 App:       $VercelUrl" -ForegroundColor White
    Write-Host "  📚 Docs:      $VercelUrl/docs" -ForegroundColor White
    Write-Host "  🏥 Health:    $VercelUrl/health" -ForegroundColor White
    Write-Host "  🎛️  Dashboard: https://vercel.com/dashboard" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "Railway:" -ForegroundColor Yellow
Write-Host "  🌐 App:       $RailwayUrl" -ForegroundColor White
Write-Host "  📚 Docs:      $RailwayUrl/docs" -ForegroundColor White
Write-Host "  🏥 Health:    $RailwayUrl/health" -ForegroundColor White
Write-Host "  🎛️  Dashboard: https://railway.app/dashboard" -ForegroundColor Cyan
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
