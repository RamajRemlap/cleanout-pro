# Railway Deployment Script
$env:RAILWAY_TOKEN = "2520b6ce-2f9d-4f69-84a7-fa2fc6aca3a9"

Write-Host "🚂 Authenticating with Railway..."
railway whoami

Write-Host "`n🚀 Initializing Railway project..."
railway init

Write-Host "`n🔧 Setting environment variables..."
railway variables set DATABASE_URL="postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

Write-Host "`n📦 Deploying to Railway..."
railway up

Write-Host "`n🌐 Getting deployment URL..."
railway domain

Write-Host "`n✅ Deployment complete!"
