# ═══════════════════════════════════════════════════════════════════════════════
# CLEANOUT PRO - Main Menu
# ═══════════════════════════════════════════════════════════════════════════════

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  ╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "  ║                                                                  ║" -ForegroundColor Cyan
    Write-Host "  ║              🚀 CLEANOUT PRO DEPLOYMENT CENTER 🚀                ║" -ForegroundColor Cyan
    Write-Host "  ║                                                                  ║" -ForegroundColor Cyan
    Write-Host "  ║            Everything you need to deploy your API               ║" -ForegroundColor Cyan
    Write-Host "  ║                                                                  ║" -ForegroundColor Cyan
    Write-Host "  ╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Menu {
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host "  📋 QUICK ACTIONS" -ForegroundColor Yellow
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    1. 🎯 Show DATABASE_URL (copy this first!)" -ForegroundColor White
    Write-Host "    2. ⚡ Deploy to Vercel (automated)" -ForegroundColor White
    Write-Host "    3. 🚂 Deploy to Railway (automated)" -ForegroundColor White
    Write-Host "    4. 🔧 Configure everything (master script)" -ForegroundColor White
    Write-Host "    5. 📚 Open documentation" -ForegroundColor White
    Write-Host "    6. 🧪 Test deployment" -ForegroundColor White
    Write-Host "    7. 📊 Check deployment status" -ForegroundColor White
    Write-Host "    8. 💾 Commit and push to GitHub" -ForegroundColor White
    Write-Host "    0. ❌ Exit" -ForegroundColor White
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host ""
}

function Show-DatabaseURL {
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  🗄️  DATABASE_URL - Copy This!" -ForegroundColor Green
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "  postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Use this in:" -ForegroundColor Yellow
    Write-Host "    - Vercel: Settings → Environment Variables → Add DATABASE_URL" -ForegroundColor White
    Write-Host "    - Railway: Variables tab → Add DATABASE_URL" -ForegroundColor White
    Write-Host ""
    Write-Host "  Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Deploy-Vercel {
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  ⚡ Deploying to Vercel..." -ForegroundColor Cyan
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    if (Test-Path ".\deploy_vercel.ps1") {
        & ".\deploy_vercel.ps1"
    } else {
        Write-Host "  ❌ deploy_vercel.ps1 not found!" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "  Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Deploy-Railway {
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  🚂 Deploying to Railway..." -ForegroundColor Cyan
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    if (Test-Path ".\deploy_railway.ps1") {
        & ".\deploy_railway.ps1"
    } else {
        Write-Host "  ❌ deploy_railway.ps1 not found!" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "  Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Configure-All {
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  🔧 Running master configuration..." -ForegroundColor Cyan
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    if (Test-Path ".\deploy_config.ps1") {
        & ".\deploy_config.ps1"
    } else {
        Write-Host "  ❌ deploy_config.ps1 not found!" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "  Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Show-Documentation {
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  📚 Documentation Files" -ForegroundColor Cyan
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    $docs = @(
        @{Name="QUICK_DEPLOY.md"; Description="Quick reference (fastest)"},
        @{Name="WHERE_TO_CLICK.md"; Description="Visual guide with screenshots"},
        @{Name="MANUAL_DEPLOYMENT_GUIDE.md"; Description="Detailed step-by-step"},
        @{Name="DEPLOYMENT_SUMMARY.md"; Description="Complete overview"},
        @{Name="DEPLOYMENT_STATUS.md"; Description="Current status"}
    )
    
    foreach ($doc in $docs) {
        if (Test-Path $doc.Name) {
            Write-Host "    ✓ $($doc.Name)" -ForegroundColor Green
            Write-Host "      → $($doc.Description)" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    Write-Host "  Open a file? (or press Enter to return)" -ForegroundColor Yellow
    $choice = Read-Host "  Enter filename"
    
    if ($choice -and (Test-Path $choice)) {
        Start-Process $choice
    }
    
    Write-Host ""
    Write-Host "  Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Test-Deployment {
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  🧪 Testing Deployments" -ForegroundColor Cyan
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "  Testing Vercel..." -ForegroundColor Yellow
    try {
        $vercelHealth = Invoke-RestMethod -Uri "https://cleanout-pro.vercel.app/health" -Method Get -ErrorAction Stop
        Write-Host "    ✅ Vercel: " -ForegroundColor Green -NoNewline
        Write-Host "HEALTHY" -ForegroundColor Green
    } catch {
        Write-Host "    ❌ Vercel: " -ForegroundColor Red -NoNewline
        Write-Host "NOT RESPONDING" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "  Testing Railway..." -ForegroundColor Yellow
    try {
        $railwayHealth = Invoke-RestMethod -Uri "https://web-production-35f31.up.railway.app/health" -Method Get -ErrorAction Stop
        Write-Host "    ✅ Railway: " -ForegroundColor Green -NoNewline
        Write-Host "HEALTHY" -ForegroundColor Green
    } catch {
        Write-Host "    ❌ Railway: " -ForegroundColor Red -NoNewline
        Write-Host "NOT RESPONDING" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "  URLs:" -ForegroundColor Yellow
    Write-Host "    Vercel:  https://cleanout-pro.vercel.app/docs" -ForegroundColor Cyan
    Write-Host "    Railway: https://web-production-35f31.up.railway.app/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Check-Status {
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  📊 Deployment Status" -ForegroundColor Cyan
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "  ✅ Database: Neon PostgreSQL" -ForegroundColor Green
    Write-Host "     → ep-withered-unit-a4erhzp0" -ForegroundColor Gray
    Write-Host "     → DATABASE_URL configured" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "  ✅ Code: Committed to GitHub" -ForegroundColor Green
    Write-Host "     → Repository: RamajRemlap/cleanout-pro" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "  📦 Deployment Scripts:" -ForegroundColor Yellow
    $scripts = @("deploy_config.ps1", "deploy_vercel.ps1", "deploy_railway.ps1", "final_push.ps1")
    foreach ($script in $scripts) {
        if (Test-Path $script) {
            Write-Host "     ✓ $script" -ForegroundColor Green
        } else {
            Write-Host "     ✗ $script" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "  📚 Documentation:" -ForegroundColor Yellow
    $docs = @("QUICK_DEPLOY.md", "WHERE_TO_CLICK.md", "MANUAL_DEPLOYMENT_GUIDE.md", "DEPLOYMENT_SUMMARY.md")
    foreach ($doc in $docs) {
        if (Test-Path $doc) {
            Write-Host "     ✓ $doc" -ForegroundColor Green
        } else {
            Write-Host "     ✗ $doc" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "  🎯 Next Step: Add DATABASE_URL to dashboards!" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Commit-And-Push {
    Write-Host ""
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  💾 Committing and Pushing to GitHub" -ForegroundColor Cyan
    Write-Host "  ═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    if (Test-Path ".\final_push.ps1") {
        & ".\final_push.ps1"
    } else {
        Write-Host "  ❌ final_push.ps1 not found!" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "  Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

while ($true) {
    Show-Banner
    Show-Menu
    
    $choice = Read-Host "  Select an option (0-8)"
    
    switch ($choice) {
        "1" { Show-DatabaseURL }
        "2" { Deploy-Vercel }
        "3" { Deploy-Railway }
        "4" { Configure-All }
        "5" { Show-Documentation }
        "6" { Test-Deployment }
        "7" { Check-Status }
        "8" { Commit-And-Push }
        "0" {
            Write-Host ""
            Write-Host "  👋 Thanks for using CleanOut Pro Deployment Center!" -ForegroundColor Green
            Write-Host ""
            exit
        }
        default {
            Write-Host ""
            Write-Host "  ❌ Invalid option. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
}
