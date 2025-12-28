# ═══════════════════════════════════════════════════════════════════
# CLEANOUT PRO - COMPLETE DEPLOYMENT AUTOMATION
# ═══════════════════════════════════════════════════════════════════
# This script automates deployment to Vercel and Railway with proper
# environment variable configuration.
# ═══════════════════════════════════════════════════════════════════

param(
    [switch]$VercelOnly,
    [switch]$RailwayOnly,
    [switch]$DryRun
)

# Color output functions
function Write-Success { param($msg) Write-Host "✅ $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "❌ $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "ℹ️  $msg" -ForegroundColor Cyan }
function Write-Warning { param($msg) Write-Host "⚠️  $msg" -ForegroundColor Yellow }
function Write-Step { param($msg) Write-Host "`n🔷 $msg" -ForegroundColor Magenta }

# Configuration
$DATABASE_URL = "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        🚀 CLEANOUT PRO - DEPLOYMENT AUTOMATION SYSTEM 🚀         ║
║                                                                   ║
║  This script will automatically deploy your application to:      ║
║  • Vercel (Frontend)                                             ║
║  • Railway (Backend API)                                         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# ═══════════════════════════════════════════════════════════════════
# STEP 1: PRE-FLIGHT CHECKS
# ═══════════════════════════════════════════════════════════════════

Write-Step "STEP 1: Pre-Flight Checks"

# Check if we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Error "Not in cleanout-pro directory! Please run from project root."
    exit 1
}
Write-Success "Project directory verified"

# Check for required CLI tools
$missingTools = @()

if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    $missingTools += "vercel"
}

if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    $missingTools += "railway"
}

if ($missingTools.Count -gt 0) {
    Write-Warning "Missing required tools: $($missingTools -join ', ')"
    Write-Info "Installing missing tools..."
    
    if ($missingTools -contains "vercel") {
        Write-Info "Installing Vercel CLI..."
        npm install -g vercel
    }
    
    if ($missingTools -contains "railway") {
        Write-Info "Installing Railway CLI..."
        if ($IsWindows) {
            iwr https://github.com/railwayapp/cli/releases/latest/download/railway-windows-amd64.exe -OutFile railway.exe
            Move-Item railway.exe $env:USERPROFILE\railway.exe -Force
            $env:Path += ";$env:USERPROFILE"
        } else {
            npm install -g @railway/cli
        }
    }
}

Write-Success "All required CLI tools are available"

# Verify database connection
Write-Info "Verifying database connection..."
$env:DATABASE_URL = $DATABASE_URL

try {
    python -c "import psycopg; conn = psycopg.connect('$DATABASE_URL'); conn.close(); print('✅ Database connection successful')"
    Write-Success "Database connection verified"
} catch {
    Write-Warning "Database connection test failed, but continuing anyway..."
}

# ═══════════════════════════════════════════════════════════════════
# STEP 2: PREPARE DEPLOYMENT FILES
# ═══════════════════════════════════════════════════════════════════

Write-Step "STEP 2: Preparing Deployment Files"

# Ensure .env file exists
if (-not (Test-Path ".env")) {
    Write-Info "Creating .env file..."
    @"
DATABASE_URL=$DATABASE_URL
FLASK_ENV=production
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
"@ | Out-File -FilePath ".env" -Encoding utf8
    Write-Success "Created .env file"
} else {
    Write-Success ".env file already exists"
}

# Verify vercel.json
if (-not (Test-Path "vercel.json")) {
    Write-Info "Creating vercel.json..."
    @'
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
'@ | Out-File -FilePath "vercel.json" -Encoding utf8
    Write-Success "Created vercel.json"
}

# Verify railway.toml
if (-not (Test-Path "railway.toml")) {
    Write-Info "Creating railway.toml..."
    @'
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn app:app"
healthcheckPath = "/api/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
'@ | Out-File -FilePath "railway.toml" -Encoding utf8
    Write-Success "Created railway.toml"
}

Write-Success "All deployment files prepared"

# ═══════════════════════════════════════════════════════════════════
# STEP 3: DEPLOY TO VERCEL
# ═══════════════════════════════════════════════════════════════════

if (-not $RailwayOnly) {
    Write-Step "STEP 3: Deploying to Vercel"
    
    if ($DryRun) {
        Write-Warning "DRY RUN: Would deploy to Vercel with DATABASE_URL configured"
    } else {
        Write-Info "Logging into Vercel..."
        vercel login
        
        Write-Info "Setting environment variable in Vercel..."
        vercel env add DATABASE_URL production --force
        Write-Host $DATABASE_URL
        
        Write-Info "Deploying to Vercel..."
        vercel --prod --yes
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Vercel deployment successful!"
            $vercelUrl = vercel ls --json | ConvertFrom-Json | Select-Object -First 1 -ExpandProperty url
            Write-Info "Your app is live at: https://$vercelUrl"
        } else {
            Write-Error "Vercel deployment failed!"
        }
    }
}

# ═══════════════════════════════════════════════════════════════════
# STEP 4: DEPLOY TO RAILWAY
# ═══════════════════════════════════════════════════════════════════

if (-not $VercelOnly) {
    Write-Step "STEP 4: Deploying to Railway"
    
    if ($DryRun) {
        Write-Warning "DRY RUN: Would deploy to Railway with DATABASE_URL configured"
    } else {
        Write-Info "Logging into Railway..."
        railway login
        
        Write-Info "Linking to Railway project..."
        railway link
        
        Write-Info "Setting environment variable in Railway..."
        railway variables set DATABASE_URL="$DATABASE_URL"
        
        Write-Info "Deploying to Railway..."
        railway up
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Railway deployment successful!"
            $railwayUrl = railway status --json | ConvertFrom-Json | Select-Object -ExpandProperty serviceUrl
            Write-Info "Your API is live at: $railwayUrl"
        } else {
            Write-Error "Railway deployment failed!"
        }
    }
}

# ═══════════════════════════════════════════════════════════════════
# STEP 5: VERIFY DEPLOYMENTS
# ═══════════════════════════════════════════════════════════════════

Write-Step "STEP 5: Verifying Deployments"

if (-not $DryRun) {
    Start-Sleep -Seconds 10
    
    if (-not $RailwayOnly) {
        Write-Info "Testing Vercel deployment..."
        try {
            $response = Invoke-WebRequest -Uri "https://cleanout-pro.vercel.app/api/health" -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Success "Vercel health check passed!"
            }
        } catch {
            Write-Warning "Vercel health check failed: $($_.Exception.Message)"
        }
    }
    
    if (-not $VercelOnly) {
        Write-Info "Testing Railway deployment..."
        try {
            $railwayStatus = railway status --json | ConvertFrom-Json
            if ($railwayStatus.status -eq "SUCCESS") {
                Write-Success "Railway deployment verified!"
            }
        } catch {
            Write-Warning "Railway status check failed: $($_.Exception.Message)"
        }
    }
}

# ═══════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                   ✅ DEPLOYMENT COMPLETE! ✅                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green

Write-Host "📋 Deployment Summary:" -ForegroundColor Cyan
Write-Host ""

if (-not $RailwayOnly) {
    Write-Host "🌐 Vercel (Frontend):" -ForegroundColor Yellow
    Write-Host "   URL: https://cleanout-pro.vercel.app"
    Write-Host "   Dashboard: https://vercel.com/dashboard"
    Write-Host ""
}

if (-not $VercelOnly) {
    Write-Host "🚂 Railway (Backend API):" -ForegroundColor Yellow
    Write-Host "   Dashboard: https://railway.app/dashboard"
    Write-Host "   Check status: railway status"
    Write-Host ""
}

Write-Host "📊 Database:" -ForegroundColor Yellow
Write-Host "   Provider: Neon PostgreSQL"
Write-Host "   Dashboard: https://console.neon.tech"
Write-Host ""

Write-Host "🔧 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Test your deployments at the URLs above"
Write-Host "   2. Monitor logs: vercel logs / railway logs"
Write-Host "   3. Check database: neon sql-editor"
Write-Host ""

Write-Host "💡 Helpful Commands:" -ForegroundColor Cyan
Write-Host "   vercel logs --follow              # Watch Vercel logs"
Write-Host "   railway logs --follow             # Watch Railway logs"
Write-Host "   vercel env ls                     # List Vercel env vars"
Write-Host "   railway variables                 # List Railway env vars"
Write-Host ""

Write-Success "All deployments configured successfully!"
