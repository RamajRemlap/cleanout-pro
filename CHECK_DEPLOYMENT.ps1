# ═══════════════════════════════════════════════════════════════════
# CLEANOUT PRO - DEPLOYMENT CHECKLIST
# ═══════════════════════════════════════════════════════════════════
# Run this script to verify your deployment setup
# ═══════════════════════════════════════════════════════════════════

# Database URL
$DATABASE_URL = "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                 CLEANOUT PRO DEPLOYMENT CHECKLIST                 ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Function to check status
function Test-Status {
    param($name, $command)
    Write-Host -NoNewline "Checking $name... "
    try {
        $result = Invoke-Expression $command
        if ($LASTEXITCODE -eq 0 -or $result) {
            Write-Host "✅ OK" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ FAILED" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

Write-Host "`n📋 VERIFICATION CHECKLIST`n" -ForegroundColor Yellow

# 1. Check CLI tools
Write-Host "1️⃣  CLI Tools:" -ForegroundColor Cyan
$vercelOk = Test-Status "Vercel CLI" "vercel --version"
$railwayOk = Test-Status "Railway CLI" "railway --version"

# 2. Check files
Write-Host "`n2️⃣  Required Files:" -ForegroundColor Cyan
$files = @("app.py", "requirements.txt", "vercel.json", "railway.toml", "Procfile")
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "❌ $file missing" -ForegroundColor Red
    }
}

# 3. Check database connection
Write-Host "`n3️⃣  Database Connection:" -ForegroundColor Cyan
$env:DATABASE_URL = $DATABASE_URL
try {
    python -c "import psycopg; conn = psycopg.connect('$DATABASE_URL'); print('✅ Connected to Neon PostgreSQL'); conn.close()"
} catch {
    Write-Host "❌ Database connection failed" -ForegroundColor Red
}

# 4. Check current deployments
Write-Host "`n4️⃣  Current Deployments:" -ForegroundColor Cyan

if ($vercelOk) {
    Write-Host "`n  Vercel Projects:" -ForegroundColor Yellow
    vercel ls 2>$null
}

if ($railwayOk) {
    Write-Host "`n  Railway Status:" -ForegroundColor Yellow
    railway status 2>$null
}

# 5. Show deployment commands
Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                    READY TO DEPLOY!                               ║
╚═══════════════════════════════════════════════════════════════════╝

🚀 QUICK DEPLOY COMMANDS:

Option 1: Deploy Everything (Recommended)
   .\DEPLOY_ALL.ps1

Option 2: Deploy Individually

   Vercel:
   vercel login
   vercel env add DATABASE_URL production
   # Paste: $DATABASE_URL
   vercel --prod

   Railway:
   railway login
   railway link
   railway variables set DATABASE_URL="$DATABASE_URL"
   railway up

Option 3: Dry Run (Test without deploying)
   .\DEPLOY_ALL.ps1 -DryRun

╔═══════════════════════════════════════════════════════════════════╗
║                    TROUBLESHOOTING                                ║
╚═══════════════════════════════════════════════════════════════════╝

If CLI tools are missing:

  Vercel:
  npm install -g vercel

  Railway:
  # Windows (PowerShell as Admin):
  iwr https://github.com/railwayapp/cli/releases/latest/download/railway-windows-amd64.exe -OutFile railway.exe
  Move-Item railway.exe C:\Windows\railway.exe

  # Or use npm:
  npm install -g @railway/cli

"@ -ForegroundColor Green

Write-Host "`n💡 TIP: Run .\DEPLOY_ALL.ps1 to deploy everything automatically!`n" -ForegroundColor Yellow
