# 🚀 Complete Deployment Guide - CleanoutPro

## Overview

Your CleanoutPro system consists of 3 components:

| Component | Technology | Deployment Target | Status |
|-----------|-----------|-------------------|--------|
| Database | PostgreSQL | **Neon.tech** | ✅ Ready |
| Backend API | FastAPI/Python | **Railway** ✅ / **Vercel** ⏳ | Railway Live |
| Desktop App | Electron | **Local Install** | ✅ Built |

---

## 1️⃣ Database: Neon PostgreSQL

### Status: ✅ Already Configured

**Connection String:**
```
postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Database Schema:**
- Location: `backend/database/schemas.sql`
- Tables: customers, jobs, rooms, invoices, pricing_rules, etc.

**No action needed** - Already set up and ready!

---

## 2️⃣ Backend API: Railway Deployment

### Status: ✅ DEPLOYED & WORKING

**Live URL:** https://web-production-35f31.up.railway.app

**Test it:**
```bash
# Health check
curl https://web-production-35f31.up.railway.app/health

# API docs
open https://web-production-35f31.up.railway.app/docs
```

**Response:**
```json
{"status":"healthy","timestamp":"2025-12-28T05:30:44.379150"}
```

### Environment Variables Already Set:
- ✅ `DATABASE_URL` - Neon connection string
- ✅ `ENVIRONMENT=production`
- ✅ `LOG_LEVEL=INFO`

**Re-deploy (if needed):**
```powershell
.\deploy_railway.ps1
```

---

## 3️⃣ Backend API: Vercel Deployment

### Status: ⏳ Ready to Deploy

**Steps to Deploy:**

### A. Via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard:**
   - https://vercel.com/dashboard

2. **Import Git Repository:**
   - Click "Add New" → "Project"
   - Import from GitHub: `cleanout-pro`
   - Root Directory: `backend`
   - Framework Preset: `Other`

3. **Configure Build Settings:**
   ```
   Build Command: (leave empty)
   Output Directory: (leave empty)
   Install Command: pip install -r requirements.txt
   ```

4. **Add Environment Variables:**
   ```
   DATABASE_URL = postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
   PYTHONUNBUFFERED = 1
   ```

5. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes

### B. Via Vercel CLI

```bash
# Login to Vercel
vercel login

# Navigate to backend
cd backend

# Deploy
vercel --prod

# Add environment variable
vercel env add DATABASE_URL production
# Paste: postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require

# Redeploy with env vars
vercel --prod
```

**After Deployment, you'll get a URL like:**
```
https://cleanout-pro-xxxxx.vercel.app
```

---

## 4️⃣ Desktop App: Local Installation

### Status: ✅ Built & Ready

**The desktop app is NOT deployed to cloud** - it's installed on users' computers!

### For Development:
```bash
cd desktop
npm install
npm start
```

### For Production Distribution:

**Build Installers:**
```bash
cd desktop
npm run build:electron
```

**Output:**
- Windows: `dist/CleanoutPro Setup.exe`
- Mac: `dist/CleanoutPro.dmg`
- Linux: `dist/CleanoutPro.AppImage`

**Distribute to Users:**
1. Upload installers to GitHub Releases
2. Or host on your website
3. Users download and install
4. App connects to Railway/Vercel API

---

## 🧪 Complete Testing Checklist

### Test 1: Database Connection
```bash
# From backend directory
cd backend
python -c "from database.connection import engine; print('✅ Database connected!' if engine else '❌ Failed')"
```

### Test 2: Railway API
```bash
# Health check
curl https://web-production-35f31.up.railway.app/health

# Root endpoint
curl https://web-production-35f31.up.railway.app/

# API docs (open in browser)
start https://web-production-35f31.up.railway.app/docs
```

### Test 3: Vercel API (after deployment)
```bash
# Replace with your Vercel URL
export VERCEL_URL="https://your-app.vercel.app"

curl $VERCEL_URL/health
curl $VERCEL_URL/
curl $VERCEL_URL/docs
```

### Test 4: Desktop App → API Integration
```bash
# Start desktop app
cd desktop
npm start

# In the app:
# 1. Go to Settings
# 2. Verify API URL is correct
# 3. Go to Dashboard - should show connection status
# 4. Go to 3D Visualization - should load demo rooms
```

---

## 🎯 End-to-End Test

### Complete Flow Test:

1. **Database:** ✅ Neon PostgreSQL running
2. **Backend (Railway):** ✅ API responding
3. **Backend (Vercel):** Deploy & test
4. **Desktop App:**
   - Install locally
   - Configure API URL
   - Test 3D visualization
   - Verify data loads

### Test Script:
```bash
# Run this to test everything
.\test_all_deployments.ps1
```

---

## 📊 Deployment Status Dashboard

Run this to check all services:

```powershell
# Check Railway
Write-Host "Testing Railway..." -ForegroundColor Yellow
curl https://web-production-35f31.up.railway.app/health

# Check Vercel (update URL after deployment)
Write-Host "Testing Vercel..." -ForegroundColor Yellow
curl https://your-app.vercel.app/health

# Check Desktop App Build
Write-Host "Testing Desktop Build..." -ForegroundColor Yellow
cd desktop
npm run build
```

---

## 🔧 Troubleshooting

### Railway Issues
```bash
# View logs
railway logs

# Check variables
railway variables

# Redeploy
railway up
```

### Vercel Issues
```bash
# View logs
vercel logs

# Check env vars
vercel env ls

# Redeploy
vercel --prod
```

### Desktop App Issues
```bash
# Clear cache
cd desktop
rm -rf node_modules
npm install

# Rebuild
npm run build
```

---

## 🎉 Success Criteria

Your deployment is successful when:

- ✅ Railway API returns 200 on `/health`
- ✅ Vercel API returns 200 on `/health`
- ✅ Desktop app connects to API
- ✅ 3D visualization shows rooms
- ✅ Database queries work

---

## 📋 Summary

**What's Deployed:**
1. ✅ Neon Database - Cloud PostgreSQL
2. ✅ Railway Backend - FastAPI serving at https://web-production-35f31.up.railway.app
3. ⏳ Vercel Backend - Deploy following steps above
4. ✅ Desktop App - Built, ready for local installation

**What Users Install:**
- Desktop App (Electron) - Downloads and runs locally
- Connects to Railway or Vercel API
- Data stored in Neon database

**Total Cost:** $0/month (all free tiers)

---

## 🚀 Quick Deploy Commands

```bash
# Deploy Railway
.\deploy_railway.ps1

# Deploy Vercel
cd backend && vercel --prod

# Build Desktop App
cd desktop && npm run build:electron

# Test Everything
.\test_all_deployments.ps1
```

**Need help?** Check the logs or run health checks above!
