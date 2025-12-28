# ═══════════════════════════════════════════════════════════════════
# CLEANOUT PRO - BROWSER AUTOMATION HELPER
# ═══════════════════════════════════════════════════════════════════
# This script opens all the necessary dashboards in your browser
# ═══════════════════════════════════════════════════════════════════

param(
    [switch]$VercelOnly,
    [switch]$RailwayOnly,
    [switch]$NeonOnly,
    [switch]$All
)

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║           🌐 CLEANOUT PRO - DASHBOARD LAUNCHER 🌐                ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Database URL for easy copying
$DATABASE_URL = "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

Write-Host "📋 Database URL copied to clipboard!" -ForegroundColor Green
Set-Clipboard -Value $DATABASE_URL

# Function to open URL
function Open-Dashboard {
    param($name, $url)
    Write-Host "🌐 Opening $name..." -ForegroundColor Cyan
    Start-Process $url
    Start-Sleep -Seconds 1
}

if ($All -or (-not $VercelOnly -and -not $RailwayOnly -and -not $NeonOnly)) {
    Write-Host @"
    
🚀 Opening all dashboards...

⏱️  I'll open them one at a time with 2-second delays.
🔑 The DATABASE_URL is already in your clipboard - just paste it!

"@ -ForegroundColor Yellow

    Start-Sleep -Seconds 2
    
    # Vercel
    Write-Host "`n1️⃣  VERCEL" -ForegroundColor Magenta
    Write-Host "   Action: Go to Settings → Environment Variables → Add New" -ForegroundColor Gray
    Open-Dashboard "Vercel Dashboard" "https://vercel.com/dashboard"
    Start-Sleep -Seconds 3
    
    # Railway
    Write-Host "`n2️⃣  RAILWAY" -ForegroundColor Magenta
    Write-Host "   Action: Select project → Variables → New Variable" -ForegroundColor Gray
    Open-Dashboard "Railway Dashboard" "https://railway.app/dashboard"
    Start-Sleep -Seconds 3
    
    # Neon
    Write-Host "`n3️⃣  NEON" -ForegroundColor Magenta
    Write-Host "   Info: Your database dashboard (for monitoring)" -ForegroundColor Gray
    Open-Dashboard "Neon Console" "https://console.neon.tech"
    
} elseif ($VercelOnly) {
    Write-Host "🌐 Opening Vercel Dashboard..." -ForegroundColor Cyan
    Write-Host "`n📝 Steps:" -ForegroundColor Yellow
    Write-Host "   1. Find 'cleanout-pro' project"
    Write-Host "   2. Click Settings"
    Write-Host "   3. Click Environment Variables"
    Write-Host "   4. Click 'Add New'"
    Write-Host "   5. Name: DATABASE_URL"
    Write-Host "   6. Value: Paste from clipboard (Ctrl+V)"
    Write-Host "   7. Check all environments"
    Write-Host "   8. Click Save"
    Write-Host "   9. Go to Deployments → Redeploy latest"
    
    Start-Sleep -Seconds 2
    Open-Dashboard "Vercel" "https://vercel.com/dashboard"
    
} elseif ($RailwayOnly) {
    Write-Host "🚂 Opening Railway Dashboard..." -ForegroundColor Cyan
    Write-Host "`n📝 Steps:" -ForegroundColor Yellow
    Write-Host "   1. Find 'cleanout-pro' project"
    Write-Host "   2. Click on your service"
    Write-Host "   3. Click Variables (left sidebar)"
    Write-Host "   4. Click '+ New Variable'"
    Write-Host "   5. Name: DATABASE_URL"
    Write-Host "   6. Value: Paste from clipboard (Ctrl+V)"
    Write-Host "   7. Click Add"
    Write-Host "   8. Wait for auto-redeploy (~3 minutes)"
    
    Start-Sleep -Seconds 2
    Open-Dashboard "Railway" "https://railway.app/dashboard"
    
} elseif ($NeonOnly) {
    Write-Host "🗄️  Opening Neon Console..." -ForegroundColor Cyan
    Write-Host "`nThis is your database dashboard for monitoring." -ForegroundColor Gray
    
    Start-Sleep -Seconds 2
    Open-Dashboard "Neon" "https://console.neon.tech"
}

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                   📋 QUICK REFERENCE                              ║
╚═══════════════════════════════════════════════════════════════════╝

DATABASE_URL (already in clipboard):
$DATABASE_URL

🎯 WHAT TO DO IN EACH DASHBOARD:

VERCEL:
1. Settings → Environment Variables
2. Add: DATABASE_URL = [paste from clipboard]
3. Deployments → Redeploy latest

RAILWAY:
1. Select project → Variables
2. Add: DATABASE_URL = [paste from clipboard]
3. Wait for auto-redeploy

NEON:
- Just monitor your database health
- No action needed

╔═══════════════════════════════════════════════════════════════════╗
║                   ⚡ AFTER ADDING VARIABLES                      ║
╚═══════════════════════════════════════════════════════════════════╝

Test your deployments:

✅ Vercel:  https://cleanout-pro.vercel.app/api/health
✅ Railway: [Get URL from Settings → Domains]/api/health

Both should return: {"status": "healthy"}

"@ -ForegroundColor Green

Write-Host "`n💡 TIP: The DATABASE_URL is in your clipboard. Just press Ctrl+V to paste it!`n" -ForegroundColor Yellow

# Save the URLs to a file for easy reference
$urlsFile = "DEPLOYMENT_URLS.txt"
@"
CLEANOUT PRO - DEPLOYMENT URLS
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

═══════════════════════════════════════════════════════════════════

DASHBOARDS:

Vercel:   https://vercel.com/dashboard
Railway:  https://railway.app/dashboard
Neon:     https://console.neon.tech

═══════════════════════════════════════════════════════════════════

DATABASE URL:

$DATABASE_URL

═══════════════════════════════════════════════════════════════════

LIVE APPS (after deployment):

Vercel App:   https://cleanout-pro.vercel.app
Health Check: https://cleanout-pro.vercel.app/api/health

Railway App:  [Check Railway Dashboard → Settings → Domains]
Health Check: [Your Railway URL]/api/health

═══════════════════════════════════════════════════════════════════

USEFUL COMMANDS:

Open Vercel:   .\OPEN_DASHBOARDS.ps1 -VercelOnly
Open Railway:  .\OPEN_DASHBOARDS.ps1 -RailwayOnly
Open Neon:     .\OPEN_DASHBOARDS.ps1 -NeonOnly
Open All:      .\OPEN_DASHBOARDS.ps1 -All

Deploy All:    .\DEPLOY_ALL.ps1
Check Status:  .\CHECK_DEPLOYMENT.ps1

"@ | Out-File -FilePath $urlsFile -Encoding UTF8

Write-Host "💾 Saved all URLs to: $urlsFile" -ForegroundColor Cyan
Write-Host ""
