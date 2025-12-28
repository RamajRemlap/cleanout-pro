# ═══════════════════════════════════════════════════════════════════
# CLEANOUT PRO - VERCEL DEPLOYMENT AUTOMATION
# ═══════════════════════════════════════════════════════════════════

$DATABASE_URL = "postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        🚀 CLEANOUT PRO - VERCEL DEPLOYMENT AUTOMATION 🚀         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Check if Vercel CLI is installed
Write-Host "🔍 Checking Vercel CLI..." -ForegroundColor Yellow
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install Vercel CLI" -ForegroundColor Red
        Write-Host "Please run manually: npm install -g vercel" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ Vercel CLI installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✅ Vercel CLI already installed" -ForegroundColor Green
}

# Verify we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Not in cleanout-pro directory!" -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 DEPLOYMENT STEPS:`n" -ForegroundColor Cyan

# Step 1: Login
Write-Host "1️⃣  Logging into Vercel..." -ForegroundColor Magenta
Write-Host "   (Browser will open for authentication)" -ForegroundColor Gray
vercel login

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Vercel login failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Logged in successfully!`n" -ForegroundColor Green

# Step 2: Navigate to backend
if (Test-Path "backend") {
    Write-Host "2️⃣  Navigating to backend directory..." -ForegroundColor Magenta
    Set-Location backend
    Write-Host "✅ In backend directory`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  No backend directory found, deploying from root" -ForegroundColor Yellow
}

# Step 3: Initial deployment
Write-Host "3️⃣  Deploying to Vercel..." -ForegroundColor Magenta
Write-Host "   This may take 2-3 minutes..." -ForegroundColor Gray

# Create vercel.json if it doesn't exist
if (-not (Test-Path "vercel.json")) {
    Write-Host "   Creating vercel.json..." -ForegroundColor Gray
    @'
{
  "version": 2,
  "builds": [
    {
      "src": "*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
'@ | Out-File -FilePath "vercel.json" -Encoding utf8
}

vercel --prod --yes

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Initial deployment complete!`n" -ForegroundColor Green

# Step 4: Add DATABASE_URL environment variable
Write-Host "4️⃣  Adding DATABASE_URL environment variable..." -ForegroundColor Magenta
Write-Host "   Setting DATABASE_URL..." -ForegroundColor Gray

# Use vercel env to set the variable
$env:VERCEL_DATABASE_URL = $DATABASE_URL
vercel env add DATABASE_URL production --force <<EOF
$DATABASE_URL
EOF

Write-Host "✅ Environment variable added!`n" -ForegroundColor Green

# Step 5: Redeploy with environment variable
Write-Host "5️⃣  Redeploying with environment variable..." -ForegroundColor Magenta
Write-Host "   This may take 2-3 minutes..." -ForegroundColor Gray

vercel --prod --yes

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Redeployment failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Deployment complete!`n" -ForegroundColor Green

# Get deployment URL
Write-Host "6️⃣  Getting deployment URL..." -ForegroundColor Magenta
$deploymentInfo = vercel ls --json | ConvertFrom-Json
$deploymentUrl = $deploymentInfo[0].url

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                    ✅ DEPLOYMENT SUCCESSFUL! ✅                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

🌐 Your Vercel URL:
   https://$deploymentUrl

📊 Testing Endpoints...

"@ -ForegroundColor Green

# Test health endpoint
Write-Host "Testing health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "https://$deploymentUrl/api/health" -Method Get
    Write-Host "✅ Health Check: " -NoNewline -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json) -ForegroundColor White
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test database endpoint
Write-Host "`nTesting database endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "https://$deploymentUrl/api/db/test" -Method Get
    Write-Host "✅ Database Test: " -NoNewline -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json) -ForegroundColor White
} catch {
    Write-Host "⚠️  Database test endpoint not available (may need to be implemented)" -ForegroundColor Yellow
}

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                    📋 DEPLOYMENT SUMMARY                          ║
╚═══════════════════════════════════════════════════════════════════╝

🌐 Vercel Dashboard: https://vercel.com/dashboard
📊 Your App: https://$deploymentUrl
🔍 Health Check: https://$deploymentUrl/api/health

✅ Next Steps:
   1. Test all API endpoints
   2. Verify database connectivity
   3. Compare with Railway deployment
   4. Update frontend to use this URL

💡 Useful Commands:
   vercel logs --follow       # View live logs
   vercel env ls              # List environment variables
   vercel --prod              # Redeploy

"@ -ForegroundColor Cyan

# Save URL to file
$deploymentUrl | Out-File -FilePath "..\VERCEL_URL.txt" -Encoding utf8
Write-Host "💾 Vercel URL saved to VERCEL_URL.txt`n" -ForegroundColor Green

Write-Host "🎉 Deployment complete! Share this URL for comprehensive testing.`n" -ForegroundColor Green
