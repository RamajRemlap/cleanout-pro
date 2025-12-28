# 🚀 Vercel CLI Deployment - Step by Step

Follow these commands **in order**:

## Step 1: Login to Vercel

```bash
vercel login
```

**What happens:**
- Browser opens automatically
- Click "Continue with GitHub" (or your preferred method)
- Authorize Vercel
- Terminal shows: "Success! Email verified."

---

## Step 2: Navigate to Backend

```bash
cd backend
```

---

## Step 3: Deploy to Production

```bash
vercel --prod
```

**You'll see prompts - answer like this:**

```
? Set up and deploy "~/backend"?
→ Press Y (Yes)

? Which scope do you want to deploy to?
→ Select your account (use arrow keys)

? Link to existing project?
→ Press N (No - create new)

? What's your project's name?
→ Type: cleanoutpro-backend (or press Enter for default)

? In which directory is your code located?
→ Press Enter (defaults to ./)

? Override settings?
→ Press N (No)
```

**Deployment starts!** Takes 1-2 minutes.

**Output will show:**
```
✅ Production: https://cleanoutpro-backend-xxxxx.vercel.app [2m]
```

**COPY THIS URL!** You'll need it.

---

## Step 4: Add Environment Variable

```bash
vercel env add DATABASE_URL production
```

**When prompted for value, paste this EXACTLY:**
```
postgresql+psycopg://neondb_owner:npg_p9mhiKgMyQ3Y@ep-withered-unit-a4erhzp0-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

Press Enter.

**Output:**
```
✅ Added Environment Variable DATABASE_URL to Project cleanoutpro-backend
```

---

## Step 5: Redeploy with Environment Variable

```bash
vercel --prod
```

This time it's faster (30 seconds) because it just rebuilds with the new env var.

**New URL appears:**
```
✅ Production: https://cleanoutpro-backend-xxxxx.vercel.app [30s]
```

---

## Step 6: Test Deployment

**Copy your Vercel URL from Step 5, then run:**

```bash
# Test health endpoint
curl https://your-vercel-url.vercel.app/health

# Test root endpoint
curl https://your-vercel-url.vercel.app/

# Open API docs in browser
start https://your-vercel-url.vercel.app/docs
```

---

## 🎉 Success!

Your backend is now deployed to Vercel!

**What you have now:**
- ✅ Railway: https://web-production-35f31.up.railway.app
- ✅ Vercel: https://your-app.vercel.app
- ✅ Both connected to same Neon database
- ✅ Desktop app can use either URL

---

## 📊 Quick Commands

```bash
# View deployment logs
vercel logs

# List all deployments
vercel ls

# Open project dashboard
vercel open

# Check environment variables
vercel env ls
```

---

## ⚠️ Troubleshooting

**If login fails:**
```bash
vercel logout
vercel login
```

**If deployment fails:**
```bash
# Check logs
vercel logs

# Try again
vercel --prod
```

**If environment variable not working:**
```bash
# List variables to verify
vercel env ls

# Remove and re-add
vercel env rm DATABASE_URL production
vercel env add DATABASE_URL production
# Paste the connection string again
```

---

## 🔗 Useful Links

- Dashboard: https://vercel.com/dashboard
- Docs: https://vercel.com/docs
- CLI Reference: https://vercel.com/docs/cli

---

**After completing all steps, give me your Vercel URL and I'll run comprehensive tests!**
