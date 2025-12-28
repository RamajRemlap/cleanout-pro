# iPhone Setup Guide - CleanoutPro Mobile App

## Current Status

⚠️ **The mobile app is not yet built.** This guide explains what needs to happen before you can use CleanoutPro on your iPhone.

## What You Need

### For Development (Building the App)
1. **Mac computer** with macOS (required for iOS development)
2. **Xcode** (free from Mac App Store)
3. **Node.js** and npm installed
4. **React Native CLI**: `npm install -g react-native-cli`
5. **CocoaPods**: `sudo gem install cocoapods`
6. **Apple Developer Account** ($99/year for App Store distribution, or free for personal testing)

### For End Users (Once App is Built)
- **Option 1**: Download from App Store (requires published app)
- **Option 2**: TestFlight beta testing (requires developer invitation)
- **Option 3**: Install via Xcode (development builds only)

## Quick Start Options

### Option A: I Want to Build the Mobile App Now

If you're a developer and want to create the React Native mobile app:

```bash
# 1. Install React Native CLI globally
npm install -g react-native-cli

# 2. Create the mobile app
npx react-native init CleanoutProMobile --template react-native-template-typescript

# 3. Move into mobile directory
cd CleanoutProMobile

# 4. Install iOS dependencies
cd ios && pod install && cd ..

# 5. Run on iOS simulator (requires Mac + Xcode)
npx react-native run-ios

# 6. Or run on physical iPhone (requires Apple Developer account)
# - Open ios/CleanoutProMobile.xcworkspace in Xcode
# - Connect iPhone via USB
# - Select your device in Xcode
# - Click "Run" button
```

**Key Features to Implement**:
- 📷 Camera integration for room photos
- 🔄 Offline mode with local queue sync
- 📍 GPS location capture for job sites
- 📊 Display AI classification results
- ✅ Simple UI for field workers (minimal distractions)

### Option B: Use the Backend API Directly (Testing)

For now, you can test the backend API from any HTTP client on your iPhone:

**Recommended Apps**:
- **Postman** (free, available on App Store)
- **HTTP Request Test** (free)
- **REST API Client** (free)

**Example API Calls**:

```bash
# Your backend URL (update with your deployment)
BASE_URL="https://your-backend.railway.app"

# 1. Create a customer
POST ${BASE_URL}/api/customers
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234",
  "address": "123 Main St"
}

# 2. Create a job
POST ${BASE_URL}/api/jobs
{
  "customer_id": 1,
  "address": "123 Main St",
  "status": "scheduled"
}

# 3. Classify a room (upload photo)
POST ${BASE_URL}/api/rooms/classify
Content-Type: multipart/form-data
- job_id: 1
- room_name: "Master Bedroom"
- image: [select photo from iPhone]
```

### Option C: Use Web Browser (Temporary Solution)

If you need immediate access, you can create a **Progressive Web App (PWA)**:

1. Deploy backend API (already done if using Railway/Render)
2. Create simple mobile-friendly HTML interface
3. Access via Safari on iPhone
4. Add to Home Screen for app-like experience

Would you like me to create a quick PWA interface?

## Development Roadmap

To get a full iPhone app, here's what needs to be built:

### Phase 1: Core Mobile App (2-3 weeks)
- [ ] React Native project setup
- [ ] Camera integration (react-native-camera)
- [ ] Photo upload to backend API
- [ ] Display AI classification results
- [ ] Basic navigation (Home → Job → Room → Camera)

### Phase 2: Offline Mode (1-2 weeks)
- [ ] Local storage (AsyncStorage or SQLite)
- [ ] Sync queue implementation
- [ ] Background sync when online
- [ ] Conflict resolution UI

### Phase 3: Production Ready (1-2 weeks)
- [ ] Push notifications (job assignments)
- [ ] GPS location tracking
- [ ] App icons and splash screens
- [ ] TestFlight beta testing
- [ ] App Store submission

## Architecture: How Mobile App Works

```
┌─────────────────────────────────────────┐
│         iPhone Camera                    │
│  1. Field worker takes room photo        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    React Native Mobile App               │
│  2. Upload to /api/rooms/classify        │
│  3. Show loading indicator...            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Backend API (FastAPI)                 │
│  4. Ollama LLaVA analyzes image          │
│  5. Returns: size, workload, cost        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Mobile App Shows Results              │
│  ✓ Room: Master Bedroom                 │
│  ✓ Size: Large                           │
│  ✓ Workload: Heavy                       │
│  ✓ Estimate: $450                        │
└─────────────────────────────────────────┘
```

## API Endpoints You'll Use

All endpoints accept JSON and return JSON responses:

### Job Management
- `GET /api/jobs` - List all jobs
- `GET /api/jobs/{id}` - Get job details
- `POST /api/jobs` - Create new job
- `PUT /api/jobs/{id}` - Update job

### Room Classification
- `POST /api/rooms/classify` - Upload photo + classify
- `GET /api/jobs/{id}/rooms` - List rooms for job
- `PUT /api/rooms/{id}` - Update room details

### Sync (Offline Mode)
- `POST /api/sync/upload` - Upload queued operations
- `GET /api/sync/download` - Get latest data

See `API_QUICKSTART.md` for full API documentation.

## Testing on Physical iPhone

### Method 1: USB + Xcode (Free, Development Only)
1. Connect iPhone to Mac via USB
2. Open project in Xcode: `open ios/CleanoutProMobile.xcworkspace`
3. Select your device from device menu
4. Trust computer on iPhone when prompted
5. Click "Run" (▶️) button in Xcode
6. App installs and launches automatically

**Limitations**:
- Expires after 7 days (free developer account)
- Must reinstall weekly
- Can't share with others

### Method 2: TestFlight (Best for Beta Testing)
1. Enroll in Apple Developer Program ($99/year)
2. Archive app in Xcode
3. Upload to App Store Connect
4. Add beta testers via email
5. Testers receive invite link → download TestFlight app → install your app

**Benefits**:
- Lasts 90 days
- Easy to share with team
- Push updates remotely
- Collect feedback

### Method 3: App Store (Production)
1. Complete app development
2. Create App Store listing (screenshots, description)
3. Submit for Apple review (1-3 days)
4. Once approved, anyone can download

## Minimum Backend Requirements

Your backend must be accessible from iPhone:

✅ **Required**:
- HTTPS (not HTTP) - iOS requires secure connections
- Public URL (not localhost)
- CORS enabled for mobile app domain

✅ **Current Backend Status**:
- Backend is deployed (check `DEPLOYMENT_STATUS.md`)
- API endpoints ready at `/api/jobs`, `/api/rooms`, etc.
- CORS configured in `backend/api/main.py`

## Estimated Costs

| Item | Cost | Notes |
|------|------|-------|
| **Development** | $0-5,000 | Free if you build yourself, $3-5k if hiring developer |
| **Apple Developer Account** | $99/year | Required for TestFlight and App Store |
| **Backend Hosting** | $0-20/month | Railway/Render free tier works for MVP |
| **AI Processing** | $0 | Using local Ollama (self-hosted) |

## Next Steps

**Pick one**:

1. **"I want to build this now"** → I can help you:
   - Set up React Native project structure
   - Implement camera + upload functionality
   - Connect to your backend API
   - Create offline sync logic

2. **"I just want to test the backend"** → I can create:
   - Simple web interface you can use in Safari
   - Progressive Web App (PWA) that works like an app
   - Postman collection for API testing

3. **"I need to hire a developer"** → I can provide:
   - Technical specification document
   - API integration guide
   - UI/UX wireframes
   - Development timeline estimate

**What would you like to do?**
