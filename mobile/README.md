# CleanoutPro Mobile App

AI-powered mobile app for junk removal field workers. Capture room photos → AI analyzes → Get instant estimates.

## Features

- 📷 **Camera Capture**: Professional camera interface with guided frame
- 🤖 **AI Vision**: Automatic room size and workload classification via Ollama LLaVA
- 💰 **Instant Estimates**: Real-time pricing based on AI analysis
- 📱 **Offline Mode**: Works offline with automatic sync when online
- ✅ **Human Override**: Desktop staff can verify and adjust AI classifications

## Prerequisites

- Node.js 18+
- React Native development environment
  - For iOS: Xcode, CocoaPods
  - For Android: Android Studio, Java JDK
- Backend API running (see `../backend/README.md`)

## Installation

```bash
# Install dependencies
npm install

# iOS only - Install pods
cd ios && pod install && cd ..
```

## Configuration

Create `.env` file:

```bash
cp .env.example .env
```

Update `API_URL` to point to your backend:

```env
# For Android emulator
API_URL=http://10.0.2.2:8000

# For iOS simulator
API_URL=http://localhost:8000

# For physical device (use your machine's IP)
API_URL=http://192.168.1.100:8000

# For production
API_URL=https://your-backend-url.com
```

## Running the App

### Android

```bash
npm run android
```

### iOS

```bash
npm run ios
```

### Development Mode

```bash
# Start Metro bundler
npm start
```

## Camera Permissions

The app requires camera permissions to capture room photos.

### Android

Add to `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
```

### iOS

Add to `ios/YourAppName/Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>We need camera access to capture room photos for estimates</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>We need photo library access to select existing photos</string>
```

## Usage Flow

1. **Select Job**: Choose active job from list
2. **Add Room**: Tap "Add Room" button
3. **Capture Photo**: Frame room in guide and capture
4. **Enter Details**: Name the room (e.g., "Master Bedroom")
5. **Upload**: Photo uploaded to backend, AI analyzes
6. **View Results**: See AI classification, confidence, and estimate
7. **Repeat**: Add more rooms to complete job estimate

## Offline Mode

The app works offline:

- Room photos stored locally
- Operations queued for sync
- Auto-syncs when connection restored
- Badge shows pending sync count

## Architecture

```
mobile/
├── src/
│   ├── components/
│   │   └── CameraCapture.tsx    # Camera UI component
│   ├── screens/
│   │   ├── JobListScreen.tsx    # Job selection
│   │   ├── RoomListScreen.tsx   # Room gallery
│   │   ├── CaptureScreen.tsx    # Photo capture flow
│   │   └── RoomDetailScreen.tsx # AI results
│   ├── services/
│   │   ├── api.ts               # Backend API client
│   │   └── sync.ts              # Offline sync queue
│   ├── store/
│   │   └── index.ts             # Global state (Zustand)
│   └── types/
│       └── index.ts             # TypeScript types
├── App.tsx                       # Navigation setup
└── index.js                      # Entry point
```

## Key Libraries

- **react-navigation**: Navigation stack
- **react-native-vision-camera**: Professional camera
- **react-native-image-picker**: Gallery picker
- **axios**: HTTP client
- **zustand**: State management
- **@react-native-async-storage/async-storage**: Local storage

## Troubleshooting

### Camera not working

```bash
# Android - Check permissions
adb shell pm list permissions -d -g

# iOS - Reset simulator
Device → Erase All Content and Settings
```

### Backend connection failed

```bash
# Test backend health
curl http://localhost:8000/health

# Check API_URL in .env
cat .env

# Android emulator - Use 10.0.2.2 instead of localhost
```

### Build errors

```bash
# Clean build
cd android && ./gradlew clean && cd ..
cd ios && pod deintegrate && pod install && cd ..

# Clear Metro cache
npm start -- --reset-cache
```

## Production Build

### Android APK

```bash
cd android
./gradlew assembleRelease
# APK: android/app/build/outputs/apk/release/app-release.apk
```

### iOS IPA

```bash
# Open Xcode
open ios/YourAppName.xcworkspace

# Product → Archive → Distribute App
```

## License

Proprietary - CleanoutPro
