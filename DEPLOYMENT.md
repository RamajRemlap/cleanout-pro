# CleanoutPro Backend Deployment Guide

## Deploy to Railway (Recommended)

### Prerequisites
- GitHub account
- Railway account (https://railway.app) - Free tier available

### Step 1: Push to GitHub

```bash
# Create a new repository on GitHub: cleanout-pro

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/cleanout-pro.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `cleanout-pro` repository
5. Railway will auto-detect the configuration

### Step 3: Configure Environment Variables

In Railway dashboard, add these variables:

```
DATABASE_URL=postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
OLLAMA_URL=http://host.docker.internal:11434
REDIS_URL=redis://red-xxxxx:6379
```

### Step 4: Deploy

Railway will automatically deploy. Your API will be available at:
```
https://YOUR_APP.railway.app
```

### Step 5: Test Deployment

```bash
curl https://YOUR_APP.railway.app/health
curl https://YOUR_APP.railway.app/docs
```

---

## Deploy to Render (Alternative)

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Render

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: cleanout-pro-api
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

### Step 3: Environment Variables

Add in Render dashboard:
```
DATABASE_URL=postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
OLLAMA_URL=http://localhost:11434
```

### Step 4: Deploy

Click "Create Web Service" - Render will deploy automatically.

---

## Environment Variables Explained

- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `OLLAMA_URL`: AI vision service (not available in free tier - will fail gracefully)
- `REDIS_URL`: Optional caching layer (Railway can provision automatically)

## Post-Deployment

### Test Endpoints
```bash
# Health check
curl https://YOUR_DEPLOYED_URL/health

# API docs
open https://YOUR_DEPLOYED_URL/docs

# Create a job
curl -X POST https://YOUR_DEPLOYED_URL/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "d146f672-b212-40e7-ba73-7dc2aa94d5cc", "property_address": "123 Main St"}'
```

### Update Mobile/Desktop Apps

Update the API URL in your mobile and desktop apps to point to:
```
https://YOUR_DEPLOYED_URL
```

## Troubleshooting

### Database Connection Issues
- Ensure `sslmode=require` is in DATABASE_URL
- Check Neon dashboard - database must be active
- Verify connection string is correct

### Build Failures
- Check Railway/Render logs
- Ensure `requirements.txt` is in `backend/` directory
- Verify Python version compatibility (3.11)

### API Not Responding
- Check deployment logs
- Verify PORT environment variable is set
- Ensure start command includes `--port $PORT`

## Free Tier Limits

**Railway**:
- $5 free credits/month
- 500 hours execution time
- Shared CPU/RAM

**Render**:
- Free tier spins down after 15 min inactivity
- 750 hours/month
- Shared resources

## Next Steps

1. Set up custom domain (optional)
2. Configure CI/CD for automatic deployments
3. Add monitoring (Railway/Render built-in)
4. Set up staging environment
5. Configure CORS for production domains
