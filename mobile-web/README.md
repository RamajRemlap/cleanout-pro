# CleanoutPro Mobile Web App (PWA)

## What is This?

A **Progressive Web App** that works on your iPhone's Safari browser - no App Store needed!

This is a lightweight, mobile-friendly web interface that lets field workers:
- 📷 Capture room photos using iPhone camera
- 🤖 Get AI-powered size/workload classification
- 💰 See instant price estimates
- 📱 Add to home screen like a native app

## How to Use on iPhone

### Step 1: Deploy This Web App

**Option A: Using GitHub Pages (Free)**
```bash
# Push this folder to a GitHub repo
git add mobile-web/
git commit -m "Add mobile web app"
git push

# Enable GitHub Pages:
# 1. Go to repo Settings → Pages
# 2. Source: Deploy from branch → main → /mobile-web
# 3. Your URL: https://yourusername.github.io/cleanout-pro/
```

**Option B: Using Netlify/Vercel (Free)**
```bash
# Drag and drop the mobile-web folder to:
# - netlify.com/drop
# - vercel.com
```

**Option C: Serve from Your Backend**
```bash
# Copy mobile-web/ folder to your backend server
# Serve as static files from FastAPI (already configured if using Railway)
```

### Step 2: Open in Safari

1. Open Safari on your iPhone
2. Go to your deployed URL (e.g., `https://yourapp.netlify.app`)
3. Tap the **Share** button (⎘ square with arrow)
4. Scroll down and tap **"Add to Home Screen"**
5. Tap **"Add"** in the top right
6. Icon appears on your home screen! 🎉

### Step 3: Configure API

1. Open the app from your home screen
2. Enter your backend API URL in settings
   - Example: `https://your-backend.railway.app`
3. Tap "Save Settings"

### Step 4: Start Using

1. Tap **"Load Jobs"** to see available jobs
2. Select a job from the list
3. Enter room name (e.g., "Master Bedroom")
4. Tap **"Take Photo"** → Camera opens
5. Capture the room
6. Tap **"Classify & Estimate"**
7. Wait 10-30 seconds for AI processing
8. View results: Size, Workload, Cost estimate

## Features

✅ **Works Offline** - Service worker caches the app
✅ **Native Camera** - Full access to iPhone camera
✅ **Home Screen Icon** - Looks like a real app
✅ **No App Store** - Deploy instantly, no review process
✅ **Auto-updates** - Changes deploy immediately
✅ **Lightweight** - Single HTML file, ~15KB

## Limitations

❌ No push notifications (native app only)
❌ No background GPS tracking
❌ Requires internet for API calls (offline mode limited)
❌ Can't access advanced iOS features

## Deployment Options

| Platform | Cost | Setup Time | URL Example |
|----------|------|------------|-------------|
| **GitHub Pages** | Free | 2 min | `username.github.io/cleanout-pro` |
| **Netlify** | Free | 1 min | `yourapp.netlify.app` |
| **Vercel** | Free | 1 min | `yourapp.vercel.app` |
| **Your Backend** | Included | 5 min | `your-backend.railway.app` |

## Customization

### Change Colors
Edit `index.html` line 16-18:
```css
.header {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
}
```

### Add Logo
Replace icon placeholder files:
- `icon-192.png` (192x192px)
- `icon-512.png` (512x512px)

### Add Features
The code is well-commented - customize as needed!

## Testing Locally

```bash
# Serve with Python
cd mobile-web
python -m http.server 8080

# Open in browser
# http://localhost:8080
```

## Support

- Works on iOS 11.3+ (Safari)
- Works on Android (Chrome)
- Desktop browsers supported (for testing)

## Next Steps

This PWA is a **temporary solution** while you build a full React Native app. It's perfect for:
- Immediate field testing
- Proof of concept demos
- MVP launch

For production, consider upgrading to a native app for better performance and features.
