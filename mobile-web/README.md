# CleanoutPro Mobile Web PWA

**Progressive Web App** that works on **ANY device** with a browser - iPhone, Android, desktop. No app store needed!

## 🚀 Deploy to Netlify (1 Minute)

### Option 1: GitHub + Netlify (Recommended)

1. **Push to GitHub**:
```bash
git add mobile-web/
git commit -m "Add mobile-web PWA"
git push
```

2. **Deploy on Netlify**:
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub
   - Select your repository
   - Build settings:
     - Base directory: `mobile-web`
     - Build command: `npm run build`
     - Publish directory: `mobile-web/dist`
   - Click "Deploy"

3. **Done!** Get your URL: `https://your-app.netlify.app`

### Option 2: Netlify CLI (Fastest)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Navigate to mobile-web
cd mobile-web

# Install dependencies
npm install

# Build
npm run build

# Deploy
netlify deploy --prod
```

## 📱 Use on iPhone

1. **Open in Safari**: Visit your Netlify URL
2. **Add to Home Screen**:
   - Tap the Share button (square with arrow)
   - Scroll down and tap "Add to Home Screen"
   - Tap "Add"
3. **Launch**: Icon appears on home screen - works like a native app!

## ✨ Features

- 📷 **Camera Access** - Uses iPhone camera (requires permission)
- 🤖 **AI Vision** - Upload to backend for analysis
- 💰 **Instant Estimates** - See room classification and cost
- 📱 **Offline Support** - Works without internet (PWA)
- 🏠 **Add to Home Screen** - Install like native app
- 🔄 **Auto-update** - New versions install automatically

## 🔧 Local Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🌐 Connect to Backend

On first launch, you'll be prompted for your backend API URL:

- **Local**: `http://localhost:8000`
- **Railway**: `https://your-app.railway.app`
- **Render**: `https://your-app.onrender.com`
- **Vercel**: `https://your-app.vercel.app`

You can change this later by clicking "Change API URL" on the job list screen.

## 📸 Camera Permissions

### iOS Safari
1. Open Settings → Safari → Camera
2. Enable "Ask" or "Allow"

### Android Chrome
1. Tap the lock icon in address bar
2. Enable Camera permission

## 🎨 Customization

### Icons
Replace these files in `public/`:
- `icon-192.png` - 192x192px
- `icon-512.png` - 512x512px
- `apple-touch-icon.png` - 180x180px
- `favicon.ico` - 32x32px

### Colors
Edit `vite.config.js`:
```js
manifest: {
  theme_color: '#007AFF', // Your brand color
  background_color: '#ffffff'
}
```

## 🔒 HTTPS Required

Camera access requires HTTPS. Netlify provides free SSL certificates automatically.

For local testing with camera:
- Use `localhost` (allowed over HTTP)
- Or use `ngrok` for HTTPS tunnel

## 📦 What's Included

```
mobile-web/
├── src/
│   ├── components/
│   │   ├── Camera.jsx         # Browser camera with capture
│   │   ├── JobList.jsx        # Job selection
│   │   ├── RoomList.jsx       # Room gallery
│   │   └── RoomDetail.jsx     # AI results
│   ├── App.jsx                # Main app with routing
│   ├── store.js               # Zustand state management
│   ├── api.js                 # Backend API client
│   └── index.css              # Mobile-first styles
├── public/                     # PWA icons and assets
├── index.html                 # Entry point
├── vite.config.js             # Vite + PWA config
├── netlify.toml               # Netlify deployment
└── package.json               # Dependencies
```

## 🆚 vs React Native App

| Feature | Mobile Web PWA | React Native |
|---------|----------------|--------------|
| Deployment | 1 minute | Hours (app stores) |
| Updates | Instant | App store review |
| Install Size | ~500 KB | ~50 MB |
| Platform | iOS, Android, Desktop | iOS, Android only |
| App Store | Not needed | Required |
| Camera | ✅ Browser API | ✅ Native API |
| Offline | ✅ Service Worker | ✅ AsyncStorage |
| Performance | Good (90%) | Excellent (100%) |

**Use PWA for**: Immediate deployment, cross-platform, frequent updates
**Use React Native for**: Best performance, native features, app store presence

## 🐛 Troubleshooting

### Camera not working
- Check browser permissions (Settings → Safari → Camera)
- Must use HTTPS (or localhost)
- Try hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

### Backend connection failed
- Verify API URL is correct
- Check backend is running: `curl https://your-backend.com/health`
- Check CORS settings in backend
- Try "Change API URL" button

### PWA not installing
- Must use HTTPS
- Must have valid icons
- Clear Safari cache and try again

## 📈 Production Checklist

- [ ] Backend deployed and accessible
- [ ] API URL configured
- [ ] Camera permissions tested on iPhone
- [ ] Upload and AI classification working
- [ ] Custom icons added
- [ ] Brand colors updated
- [ ] PWA tested on home screen

## 🎯 Next Steps

1. Deploy to Netlify
2. Test on your iPhone
3. Share URL with field workers
4. Monitor usage and feedback
5. Update mobile/ React Native app for long-term

---

**Questions?** The PWA is production-ready and fully functional!
