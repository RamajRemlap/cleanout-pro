# 🚀 QUICK DEPLOYMENT REFERENCE CARD

## Copy this DATABASE_URL:
```
postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

---

## ⚡ VERCEL (3 Steps)

### Step 1: Add Environment Variable
1. Go to: https://vercel.com/dashboard
2. Click: **cleanout-pro** project
3. Go to: **Settings** → **Environment Variables**
4. Click: **Add New**
5. Enter:
   - **Name:** `DATABASE_URL`
   - **Value:** `postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require`
   - **Environment:** `Production`
6. Click: **Save**

### Step 2: Redeploy
1. Go to: **Deployments** tab
2. Click: **⋮** (three dots) on latest deployment
3. Click: **Redeploy**
4. Wait 2-3 minutes

### Step 3: Test
Open in browser: https://cleanout-pro.vercel.app/health

**Expected Result:** ✅ `{"status": "healthy"}`

---

## 🚂 RAILWAY (3 Steps)

### Step 1: Add Environment Variable
1. Go to: https://railway.app/dashboard
2. Click: **your-project**
3. Click: **Variables** tab
4. Click: **New Variable**
5. Enter:
   - **Variable:** `DATABASE_URL`
   - **Value:** `postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require`
6. Click: **Add**

### Step 2: Wait for Auto-Deploy
- Railway automatically redeploys when variables change
- Watch the **Deployments** tab
- Wait 3-5 minutes

### Step 3: Test
Open in browser: https://web-production-35f31.up.railway.app/health

**Expected Result:** ✅ `{"status": "healthy"}`

---

## 🎯 AUTOMATED DEPLOYMENT (PowerShell)

### Option 1: Vercel
```powershell
.\deploy_vercel.ps1
```

### Option 2: Railway
```powershell
.\deploy_railway.ps1
```

### Option 3: Configure Everything
```powershell
.\deploy_config.ps1
```

---

## ✅ Quick Test Commands

### Test Health
```bash
curl https://cleanout-pro.vercel.app/health
```

### Test API Docs
Open in browser:
- https://cleanout-pro.vercel.app/docs

### Test Create Job
```bash
curl -X POST https://cleanout-pro.vercel.app/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"address":"123 Main St","status":"scheduled"}'
```

---

## 🔍 Troubleshooting

### "Database connection failed"
→ Double-check DATABASE_URL is exactly:
```
postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### "502 Bad Gateway"
→ Wait 5 minutes, then refresh
→ Check logs in platform dashboard

### "Module not found"
→ Redeploy with cache cleared

---

## 📊 What's What

| Item | Purpose |
|------|---------|
| **DATABASE_URL** | Neon PostgreSQL connection |
| **backend/index.py** | Vercel entry point |
| **app.py** | Railway entry point |
| **backend/vercel.json** | Vercel config |
| **railway.toml** | Railway config |
| **Dockerfile** | Railway container |

---

## 🎉 Success Indicators

✅ Health endpoint returns `200 OK`  
✅ `/docs` shows Swagger UI  
✅ No errors in logs  
✅ Can create/read jobs  
✅ Database connected  

---

**YOU'RE NOT MESSING UP!**  
Everything is configured correctly. Just add DATABASE_URL and deploy! 🚀

---

*CleanOut Pro - Quick Reference v1.0*
