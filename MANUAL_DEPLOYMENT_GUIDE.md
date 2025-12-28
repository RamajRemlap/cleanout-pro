# 🚀 CleanOut Pro - Manual Deployment Guide

**Last Updated:** December 27, 2025  
**Status:** Ready for Production Deployment

---

## 📋 Prerequisites Checklist

- ✅ Neon PostgreSQL database created and configured
- ✅ GitHub repository set up and connected
- ✅ All code committed and pushed to main branch
- ✅ Database tables created (8 tables)
- ✅ Environment files configured

---

## 🗄️ Database Information

**Neon PostgreSQL Connection:**
```
DATABASE_URL=postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Database Details:**
- Project: old-violet-26235420
- Database: neondb
- Region: us-east-1 (AWS)
- Connection Pooling: ✅ Enabled
- SSL Mode: Required
- Tables: 8 (customers, jobs, rooms, room_items, invoices, invoice_items, payments, photos)

---

## ⚡ Option 1: Deploy to Vercel (Recommended for Serverless)

### Quick Start (Automated)
```powershell
# Run the automated deployment script
.\deploy_vercel.ps1
```

### Manual Steps

#### 1. **Login to Vercel**
- Go to https://vercel.com/dashboard
- Sign in with your GitHub account

#### 2. **Import Project (if not already done)**
- Click "Add New" → "Project"
- Select your GitHub repository: `RamajRemlap/cleanout-pro`
- Click "Import"

#### 3. **Configure Build Settings**
- **Framework Preset:** Other
- **Root Directory:** `backend`
- **Build Command:** (leave empty)
- **Output Directory:** (leave empty)
- **Install Command:** `pip install -r requirements.txt`

#### 4. **Add Environment Variables**
Go to: Settings → Environment Variables

| Name | Value | Environment |
|------|-------|-------------|
| `DATABASE_URL` | `postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require` | Production |
| `ENVIRONMENT` | `production` | Production |
| `LOG_LEVEL` | `INFO` | Production |
| `SECRET_KEY` | `your-secret-key-here` | Production |

#### 5. **Deploy**
- Go to "Deployments" tab
- Click "Redeploy" button
- Wait for build to complete (2-3 minutes)

#### 6. **Verify Deployment**
```bash
# Test health endpoint
curl https://cleanout-pro.vercel.app/health

# Test API docs
# Open in browser: https://cleanout-pro.vercel.app/docs
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-27T..."
}
```

---

## 🚂 Option 2: Deploy to Railway (Docker-based)

### Quick Start (Automated)
```powershell
# Run the automated deployment script
.\deploy_railway.ps1
```

### Manual Steps

#### 1. **Login to Railway**
- Go to https://railway.app/dashboard
- Sign in with your GitHub account

#### 2. **Create New Project (if needed)**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose `RamajRemlap/cleanout-pro`

#### 3. **Configure Service**
- Railway should auto-detect the Dockerfile
- Root Directory: `/` (project root)
- Build Command: Uses Dockerfile automatically

#### 4. **Add Environment Variables**
Go to: Variables tab

| Name | Value |
|------|-------|
| `DATABASE_URL` | `postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require` |
| `ENVIRONMENT` | `production` |
| `LOG_LEVEL` | `INFO` |
| `PORT` | `8000` |

#### 5. **Deploy**
- Railway auto-deploys after adding environment variables
- Monitor deployment in "Deployments" tab
- Wait for build to complete (3-5 minutes)

#### 6. **Get Deployment URL**
- Go to "Settings" tab
- Under "Domains", copy the generated URL
- Or use: https://web-production-35f31.up.railway.app

#### 7. **Verify Deployment**
```bash
# Test health endpoint
curl https://web-production-35f31.up.railway.app/health

# Test API docs
# Open in browser: https://web-production-35f31.up.railway.app/docs
```

---

## 🧪 Testing Your Deployment

### Health Check
```bash
# Vercel
curl https://cleanout-pro.vercel.app/health

# Railway
curl https://web-production-35f31.up.railway.app/health
```

### API Documentation
- **Vercel:** https://cleanout-pro.vercel.app/docs
- **Railway:** https://web-production-35f31.up.railway.app/docs

### Test Endpoints

#### 1. **Create a Job**
```bash
curl -X POST "https://cleanout-pro.vercel.app/api/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "address": "123 Main St",
    "scheduled_date": "2025-12-28",
    "status": "scheduled"
  }'
```

#### 2. **List Jobs**
```bash
curl https://cleanout-pro.vercel.app/api/jobs
```

#### 3. **Create a Room**
```bash
curl -X POST "https://cleanout-pro.vercel.app/api/rooms" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 1,
    "room_type": "living_room",
    "estimated_hours": 4.0,
    "estimated_cost": 200.00
  }'
```

---

## 🔧 Troubleshooting

### Issue: "Database connection failed"

**Solution:**
1. Verify DATABASE_URL is set correctly in environment variables
2. Check Neon database is running: https://console.neon.tech
3. Ensure SSL mode is set to `require`
4. Test connection locally first

### Issue: "Module not found"

**Solution:**
1. Check `requirements.txt` includes all dependencies
2. Rebuild deployment
3. Clear build cache (Vercel: Settings → Clear Cache)

### Issue: "502 Bad Gateway" (Railway)

**Solution:**
1. Check Railway logs: `railway logs`
2. Verify Dockerfile is correct
3. Ensure PORT environment variable is set to 8000
4. Check app is listening on 0.0.0.0, not 127.0.0.1

### Issue: "Build failed"

**Solution:**
1. Check build logs in deployment platform
2. Verify Python version matches runtime.txt (3.11.7)
3. Ensure all files are committed to git
4. Check for syntax errors in code

---

## 📊 Monitoring and Logs

### Vercel
```bash
# View logs (requires Vercel CLI)
vercel logs

# Or view in dashboard:
# https://vercel.com/dashboard → Project → Logs
```

### Railway
```bash
# View logs (requires Railway CLI)
railway logs

# Or view in dashboard:
# https://railway.app/dashboard → Project → Logs
```

---

## 🔄 Redeploying After Changes

### Vercel
1. Commit and push changes to GitHub
2. Vercel auto-deploys from main branch
3. Or manually redeploy: `vercel --prod`

### Railway
1. Commit and push changes to GitHub
2. Railway auto-deploys from main branch
3. Or manually redeploy: `railway up`

---

## 🔐 Security Checklist

- [ ] DATABASE_URL is stored as environment variable (not in code)
- [ ] SECRET_KEY is generated and secure
- [ ] SSL is enabled for database connections
- [ ] PayPal credentials are in environment variables
- [ ] API rate limiting is configured (if needed)
- [ ] CORS is properly configured

---

## 📞 Support Resources

### Documentation
- **Vercel:** https://vercel.com/docs
- **Railway:** https://docs.railway.app
- **Neon:** https://neon.tech/docs
- **FastAPI:** https://fastapi.tiangolo.com

### Dashboard Links
- **Vercel:** https://vercel.com/dashboard
- **Railway:** https://railway.app/dashboard
- **Neon:** https://console.neon.tech

---

## ✅ Deployment Success Checklist

After deployment, verify:

- [ ] Health endpoint returns 200 OK
- [ ] API documentation loads (/docs)
- [ ] Database connection works
- [ ] Can create a job
- [ ] Can list jobs
- [ ] Can create a room
- [ ] Environment variables are set
- [ ] Logs show no errors
- [ ] SSL certificate is valid
- [ ] Domain is accessible

---

## 🎉 You're Live!

Your CleanOut Pro API is now deployed and ready to use!

**Vercel URL:** https://cleanout-pro.vercel.app  
**Railway URL:** https://web-production-35f31.up.railway.app

**Next Steps:**
1. Configure your frontend to use the API URL
2. Set up PayPal credentials for payment processing
3. Add custom domain (optional)
4. Set up monitoring and alerts
5. Configure CI/CD for automated deployments

---

**Need Help?**  
Check the logs, review the troubleshooting section, or consult the platform documentation.

---

*Generated by CleanOut Pro Deployment System*  
*Last Updated: December 27, 2025*
