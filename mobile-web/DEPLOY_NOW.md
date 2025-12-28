# 🚀 Deploy to Netlify NOW (1 Minute)

## Method 1: Netlify Drop (Easiest - No CLI)

1. **Build locally**:
```bash
cd mobile-web
npm install
npm run build
```

2. **Drag & Drop**:
   - Go to https://app.netlify.com/drop
   - Drag the `dist/` folder onto the page
   - **Done!** Get your URL instantly

3. **Use on iPhone**:
   - Open URL in Safari
   - Tap Share → Add to Home Screen
   - Launch from home screen!

## Method 2: Netlify CLI (For Auto-Updates)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Navigate to mobile-web
cd mobile-web

# Install and build
npm install
npm run build

# Deploy to production
netlify deploy --prod
```

Follow prompts:
- Create & configure new site? **Yes**
- Publish directory: `dist`

**Done!** Future deploys: Just run `netlify deploy --prod`

## Method 3: GitHub + Netlify (Best for Teams)

1. **Push to GitHub**:
```bash
git add .
git commit -m "Add mobile web PWA"
git push
```

2. **Connect Netlify**:
   - Go to https://app.netlify.com
   - Click "Add new site"
   - Choose GitHub repo
   - Settings:
     - Base: `mobile-web`
     - Build: `npm run build`
     - Publish: `mobile-web/dist`
   - Deploy!

3. **Auto-deploys**: Every git push auto-deploys

## ⚙️ Configure Backend URL

After deployment, on first app open:
- You'll be prompted for API URL
- Enter your backend URL (Railway, Render, Vercel, etc.)
- Saved in browser localStorage

## 📱 Add to iPhone Home Screen

1. Open site in **Safari** (not Chrome!)
2. Tap **Share button** (square with ↑)
3. Scroll and tap **"Add to Home Screen"**
4. Name it "CleanoutPro"
5. Tap **"Add"**

**Icon appears on home screen** - launches full screen like a native app!

## ✅ Test Checklist

- [ ] Open site on iPhone
- [ ] Allow camera permissions
- [ ] Connect to backend
- [ ] View jobs list
- [ ] Capture room photo
- [ ] See AI classification
- [ ] Add to home screen
- [ ] Launch from home screen

## 🎯 Your URLs

After deployment, you'll get:
- **Netlify URL**: `https://your-app.netlify.app`
- **Custom domain** (optional): `https://cleanoutpro.com`

Share with field workers immediately!

---

**Estimated time**: 1-3 minutes ⚡
