# ═══════════════════════════════════════════════════════════════════
# CLEANOUT PRO - VERCEL DEPLOYMENT TESTER
# ═══════════════════════════════════════════════════════════════════

param(
    [Parameter(Mandatory=$true)]
    [string]$VercelUrl,
    [string]$RailwayUrl = ""
)

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║          🧪 CLEANOUT PRO - DEPLOYMENT TESTING SUITE 🧪           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Clean URL (remove https:// if present)
$VercelUrl = $VercelUrl -replace '^https?://', ''
$baseUrl = "https://$VercelUrl"

Write-Host "🎯 Testing Vercel Deployment: $baseUrl`n" -ForegroundColor Yellow

# Test results
$results = @{
    "Health Check" = $false
    "Database Connection" = $false
    "CORS Headers" = $false
    "Response Time" = 0
    "Status Code" = 0
}

# Function to test endpoint
function Test-Endpoint {
    param($name, $url, $method = "GET", $body = $null)
    
    Write-Host "Testing: $name" -ForegroundColor Cyan
    Write-Host "  URL: $url" -ForegroundColor Gray
    
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        
        if ($body) {
            $response = Invoke-WebRequest -Uri $url -Method $method -Body ($body | ConvertTo-Json) -ContentType "application/json" -UseBasicParsing
        } else {
            $response = Invoke-WebRequest -Uri $url -Method $method -UseBasicParsing
        }
        
        $stopwatch.Stop()
        $responseTime = $stopwatch.ElapsedMilliseconds
        
        Write-Host "  ✅ Status: $($response.StatusCode)" -ForegroundColor Green
        Write-Host "  ⏱️  Response Time: $responseTime ms" -ForegroundColor Gray
        
        if ($response.Content) {
            try {
                $json = $response.Content | ConvertFrom-Json
                Write-Host "  📄 Response:" -ForegroundColor Gray
                Write-Host "     $($json | ConvertTo-Json -Compress)" -ForegroundColor White
            } catch {
                Write-Host "  📄 Response: $($response.Content.Substring(0, [Math]::Min(100, $response.Content.Length)))..." -ForegroundColor White
            }
        }
        
        Write-Host ""
        return @{
            Success = $true
            StatusCode = $response.StatusCode
            ResponseTime = $responseTime
            Content = $response.Content
            Headers = $response.Headers
        }
        
    } catch {
        Write-Host "  ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                    ENDPOINT TESTS                                 " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# Test 1: Health Check
$healthResult = Test-Endpoint -name "Health Check" -url "$baseUrl/api/health"
$results["Health Check"] = $healthResult.Success

# Test 2: Root endpoint
$rootResult = Test-Endpoint -name "Root Endpoint" -url "$baseUrl/"

# Test 3: Database test
$dbResult = Test-Endpoint -name "Database Connection" -url "$baseUrl/api/db/test"
$results["Database Connection"] = $dbResult.Success

# Test 4: Properties endpoint
$propsResult = Test-Endpoint -name "Properties List" -url "$baseUrl/api/properties"

# Test 5: Analytics endpoint
$analyticsResult = Test-Endpoint -name "Analytics" -url "$baseUrl/api/analytics"

# Test 6: CORS Check
Write-Host "Testing: CORS Headers" -ForegroundColor Cyan
if ($healthResult.Headers) {
    $corsHeader = $healthResult.Headers["Access-Control-Allow-Origin"]
    if ($corsHeader) {
        Write-Host "  ✅ CORS Header Present: $corsHeader" -ForegroundColor Green
        $results["CORS Headers"] = $true
    } else {
        Write-Host "  ⚠️  CORS Header Missing" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ No headers available" -ForegroundColor Red
}
Write-Host ""

# Performance Summary
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                    PERFORMANCE METRICS                            " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

if ($healthResult.Success) {
    $avgResponseTime = $healthResult.ResponseTime
    Write-Host "  Average Response Time: $avgResponseTime ms" -ForegroundColor White
    
    if ($avgResponseTime -lt 500) {
        Write-Host "  ⚡ Performance: Excellent (< 500ms)" -ForegroundColor Green
    } elseif ($avgResponseTime -lt 1000) {
        Write-Host "  ✅ Performance: Good (< 1s)" -ForegroundColor Yellow
    } else {
        Write-Host "  ⚠️  Performance: Slow (> 1s)" -ForegroundColor Red
    }
}
Write-Host ""

# Test Results Summary
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                    TEST RESULTS SUMMARY                           " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

$passedTests = 0
$totalTests = 0

foreach ($test in $results.Keys) {
    $totalTests++
    if ($results[$test]) {
        Write-Host "  ✅ $test" -ForegroundColor Green
        $passedTests++
    } else {
        Write-Host "  ❌ $test" -ForegroundColor Red
    }
}

Write-Host "`n  Score: $passedTests / $totalTests tests passed" -ForegroundColor Cyan
Write-Host ""

# Compare with Railway if URL provided
if ($RailwayUrl) {
    Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "              VERCEL vs RAILWAY COMPARISON                         " -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan
    
    $railwayUrl = "https://$($RailwayUrl -replace '^https?://', '')"
    
    Write-Host "Testing Railway deployment: $railwayUrl`n" -ForegroundColor Yellow
    
    $railwayHealth = Test-Endpoint -name "Railway Health Check" -url "$railwayUrl/api/health"
    
    if ($healthResult.Success -and $railwayHealth.Success) {
        Write-Host "`n  📊 Performance Comparison:" -ForegroundColor Cyan
        Write-Host "     Vercel:  $($healthResult.ResponseTime) ms" -ForegroundColor White
        Write-Host "     Railway: $($railwayHealth.ResponseTime) ms" -ForegroundColor White
        
        $faster = if ($healthResult.ResponseTime -lt $railwayHealth.ResponseTime) { "Vercel" } else { "Railway" }
        $difference = [Math]::Abs($healthResult.ResponseTime - $railwayHealth.ResponseTime)
        
        Write-Host "`n     🏆 Winner: $faster (${difference}ms faster)" -ForegroundColor Green
    }
    Write-Host ""
}

# Final Deployment Report
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                    DEPLOYMENT REPORT                              " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

$reportPath = "VERCEL_TEST_REPORT.txt"
$report = @"
CLEANOUT PRO - VERCEL DEPLOYMENT TEST REPORT
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

═══════════════════════════════════════════════════════════════════

DEPLOYMENT URL:
$baseUrl

TEST RESULTS:
$(foreach ($test in $results.Keys) { "- $test: $(if ($results[$test]) { 'PASS' } else { 'FAIL' })" })

SCORE: $passedTests / $totalTests tests passed

PERFORMANCE:
- Average Response Time: $($healthResult.ResponseTime) ms
- Health Check: $($healthResult.StatusCode)
- Database: $(if ($dbResult.Success) { 'Connected' } else { 'Failed' })

ENDPOINTS TESTED:
- Health Check: $baseUrl/api/health
- Root: $baseUrl/
- Database Test: $baseUrl/api/db/test
- Properties: $baseUrl/api/properties
- Analytics: $baseUrl/api/analytics

═══════════════════════════════════════════════════════════════════

RECOMMENDATIONS:

$(if ($results["Health Check"]) { "✅" } else { "❌" }) Health endpoint is working
$(if ($results["Database Connection"]) { "✅" } else { "⚠️ "}) Database connectivity $(if ($results["Database Connection"]) { "verified" } else { "needs attention" })
$(if ($results["CORS Headers"]) { "✅" } else { "⚠️ "}) CORS headers $(if ($results["CORS Headers"]) { "configured" } else { "may need configuration" })

$(if ($healthResult.ResponseTime -lt 500) {
    "✅ Performance is excellent (< 500ms)"
} elseif ($healthResult.ResponseTime -lt 1000) {
    "⚠️  Performance is acceptable but could be improved"
} else {
    "❌ Performance needs optimization (> 1s response time)"
})

═══════════════════════════════════════════════════════════════════

NEXT STEPS:

1. Update frontend configuration with Vercel URL
2. Configure custom domain (optional)
3. Set up monitoring and alerts
4. Review and optimize slow endpoints
5. Implement caching if needed

═══════════════════════════════════════════════════════════════════
"@

$report | Out-File -FilePath $reportPath -Encoding utf8

Write-Host "💾 Full report saved to: $reportPath" -ForegroundColor Green
Write-Host ""

# Display quick summary
if ($passedTests -eq $totalTests) {
    Write-Host "🎉 ALL TESTS PASSED! Your deployment is fully functional!" -ForegroundColor Green
} elseif ($passedTests -gt 0) {
    Write-Host "⚠️  PARTIAL SUCCESS: $passedTests/$totalTests tests passed" -ForegroundColor Yellow
    Write-Host "   Review the report for details on failed tests." -ForegroundColor Gray
} else {
    Write-Host "❌ DEPLOYMENT ISSUES: No tests passed" -ForegroundColor Red
    Write-Host "   Check the deployment logs and configuration." -ForegroundColor Gray
}

Write-Host "`n✨ Testing complete! Review the full report above.`n" -ForegroundColor Cyan
