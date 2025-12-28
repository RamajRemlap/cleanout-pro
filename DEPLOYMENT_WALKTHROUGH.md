# 🚀 CLEANOUT PRO - MANUAL DEPLOYMENT GUIDE

This guide provides step-by-step instructions for deploying to Vercel and Railway.

---

## 📋 PREREQUISITES

1. **Database URL** (already configured):
   ```
   postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

2. **CLI Tools**:
   - Vercel CLI: `npm install -g vercel`
   - Railway CLI: `npm install -g @railway/cli`

---

## 🌐 VERCEL DEPLOYMENT

### Option A: Via Vercel Dashboard (Easiest)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Login with your account

2. **Go to Your Project Settings**
   - Click on your `cleanout-pro` project
   - Click **Settings** (top navigation)

3. **Add Environment Variable**
   - Click **Environment Variables** (left sidebar)
   - Click **Add New** button
   
   **Variable Details:**
   - Name: `DATABASE_URL`
   - Value: `postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require`
   - Environment: Select **Production**, **Preview**, **Development**
   
   - Click **Save**

4. **Redeploy**
   - Go to **Deployments** tab
   - Click on the latest deployment
   - Click **⋯** (three dots) → **Redeploy**
   - Wait for deployment to complete (~2-3 minutes)

5. **Verify**
   - Visit: https://cleanout-pro.vercel.app/api/health
   - You should see: `{"status": "healthy"}`

### Option B: Via CLI

```powershell
# 1. Login
vercel login

# 2. Set environment variable
vercel env add DATABASE_URL production

# When prompted, paste:
postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require

# 3. Deploy
vercel --prod
```

---

## 🚂 RAILWAY DEPLOYMENT

### Option A: Via Railway Dashboard (Easiest)

1. **Go to Railway Dashboard**
   - Visit: https://railway.app/dashboard
   - Login with your account

2. **Select Your Project**
   - Click on `cleanout-pro` project
   - Click on the **service** (your app)

3. **Add Environment Variable**
   - Click **Variables** tab (left sidebar)
   
   **Add Variable:**
   - Click **+ New Variable**
   - Name: `DATABASE_URL`
   - Value: `postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require`
   - Click **Add**

4. **Automatic Redeploy**
   - Railway automatically redeploys when you add/change variables
   - Go to **Deployments** tab to monitor progress
   - Wait for "SUCCESS" status (~3-5 minutes)

5. **Verify**
   - Click **Settings** → Copy your **Public URL**
   - Visit: `https://your-app.railway.app/api/health`
   - You should see: `{"status": "healthy"}`

### Option B: Via CLI

```powershell
# 1. Login
railway login

# 2. Link to project (if not already linked)
railway link

# 3. Set environment variable
railway variables set DATABASE_URL="postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

# 4. Deploy (optional, auto-deploys on variable change)
railway up
```

---

## ✅ VERIFICATION CHECKLIST

After deploying to both platforms:

### Vercel
- [ ] Environment variable `DATABASE_URL` is set
- [ ] Latest deployment shows "Ready" status
- [ ] Health check: https://cleanout-pro.vercel.app/api/health returns 200 OK

### Railway
- [ ] Environment variable `DATABASE_URL` is set
- [ ] Latest deployment shows "SUCCESS" status
- [ ] Health check: https://your-app.railway.app/api/health returns 200 OK

### Database (Neon)
- [ ] Database is accessible
- [ ] Tables are created
- [ ] Connection pooling is enabled

---

## 🔧 QUICK COMMANDS REFERENCE

### Vercel
```powershell
vercel login              # Login to Vercel
vercel ls                 # List projects
vercel env ls             # List environment variables
vercel env add            # Add environment variable
vercel --prod             # Deploy to production
vercel logs               # View logs
```

### Railway
```powershell
railway login             # Login to Railway
railway link              # Link to project
railway status            # Check deployment status
railway variables         # List environment variables
railway variables set     # Set environment variable
railway up                # Deploy
railway logs              # View logs
```

---

## 🎯 ONE-CLICK DEPLOYMENT

For automated deployment, use the included PowerShell script:

```powershell
# Check prerequisites
.\CHECK_DEPLOYMENT.ps1

# Deploy everything
.\DEPLOY_ALL.ps1

# Deploy only Vercel
.\DEPLOY_ALL.ps1 -VercelOnly

# Deploy only Railway
.\DEPLOY_ALL.ps1 -RailwayOnly

# Test without deploying
.\DEPLOY_ALL.ps1 -DryRun
```

---

## 🆘 TROUBLESHOOTING

### Issue: "Command not found: vercel"
**Solution:**
```powershell
npm install -g vercel
```

### Issue: "Command not found: railway"
**Solution:**
```powershell
# Windows
iwr https://github.com/railwayapp/cli/releases/latest/download/railway-windows-amd64.exe -OutFile railway.exe
Move-Item railway.exe C:\Windows\railway.exe

# Or use npm
npm install -g @railway/cli
```

### Issue: "Database connection failed"
**Solution:**
1. Verify DATABASE_URL is correct
2. Check Neon dashboard for database status
3. Ensure SSL mode is set to `require`

### Issue: "Deployment failed"
**Solution:**
1. Check deployment logs: `vercel logs` or `railway logs`
2. Verify all required files exist:
   - `app.py`
   - `requirements.txt`
   - `vercel.json` (for Vercel)
   - `railway.toml` (for Railway)
   - `Procfile` (for Railway)

---

## 📊 MONITORING

### Vercel Analytics
- Dashboard: https://vercel.com/dashboard
- Real-time logs: `vercel logs --follow`

### Railway Metrics
- Dashboard: https://railway.app/dashboard
- Real-time logs: `railway logs --follow`

### Neon Database
- Dashboard: https://console.neon.tech
- Monitoring: Check "Monitoring" tab in Neon dashboard

---

## 🎉 SUCCESS INDICATORS

You'll know everything is working when:

1. ✅ Vercel deployment shows "Ready"
2. ✅ Railway deployment shows "SUCCESS"
3. ✅ Health endpoints return 200 OK
4. ✅ Database queries work without errors
5. ✅ No error logs in either platform

---

## 📞 SUPPORT

If you encounter issues:

1. Check the logs first (`vercel logs` / `railway logs`)
2. Verify environment variables are set correctly
3. Test database connection locally
4. Review deployment documentation:
   - Vercel: https://vercel.com/docs
   - Railway: https://docs.railway.app
   - Neon: https://neon.tech/docs

---

**Last Updated:** December 2024  
**Version:** 1.0.0
