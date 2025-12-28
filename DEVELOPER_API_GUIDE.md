# CleanoutPro API Developer Guide

## For Hiring Mobile App Developers

This document provides everything a React Native developer needs to build the CleanoutPro mobile app.

---

## Project Overview

**CleanoutPro** is an AI-powered junk removal business management system. Field workers use a mobile app to:
1. Capture room photos using their phone camera
2. Get AI-powered classification (room size + workload)
3. Receive instant pricing estimates
4. Work offline and sync when back online

**Your job**: Build the React Native mobile app (iOS + Android)

---

## Technical Stack

### Mobile App (What You'll Build)
- **Framework**: React Native 0.71+
- **Language**: TypeScript (preferred) or JavaScript
- **State Management**: Redux Toolkit or Zustand
- **Offline Storage**: AsyncStorage or SQLite
- **Camera**: react-native-camera or expo-camera
- **HTTP Client**: Axios or Fetch API
- **Navigation**: React Navigation v6

### Backend (Already Built)
- **API**: FastAPI (Python) - REST endpoints
- **Database**: PostgreSQL (hosted on Neon.tech)
- **AI**: Ollama LLaVA vision model
- **Hosting**: Railway.app or Render.com

---

## API Base URL

Replace `{BASE_URL}` with the deployed backend URL:
- **Example**: `https://cleanoutpro-production.up.railway.app`
- **Protocol**: HTTPS required (iOS blocks HTTP)

---

## Authentication

**Current Status**: No authentication implemented yet

**Future**: JWT-based authentication
- Login endpoint will return access token
- Include in header: `Authorization: Bearer {token}`
- Tokens expire after 24 hours (refresh flow TBD)

For MVP, you can skip auth and proceed directly to API calls.

---

## Core API Endpoints

### 1. Health Check

**Endpoint**: `GET /`

**Purpose**: Verify API is running

**Request**:
```bash
curl https://cleanoutpro.railway.app/
```

**Response**:
```json
{
  "message": "CleanoutPro API is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

---

### 2. List All Jobs

**Endpoint**: `GET /api/jobs`

**Purpose**: Get all jobs (for job selection screen)

**Request**:
```bash
curl https://cleanoutpro.railway.app/api/jobs
```

**Response**:
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "address": "123 Main St, Boston MA",
    "status": "scheduled",
    "base_estimate": 0.0,
    "ai_estimate": 0.0,
    "human_adjusted_estimate": 0.0,
    "final_price": 0.0,
    "created_at": "2025-01-15T10:30:00",
    "scheduled_date": "2025-01-20T09:00:00"
  },
  {
    "id": 2,
    "customer_id": 2,
    "address": "456 Oak Ave, Cambridge MA",
    "status": "in_progress",
    "base_estimate": 850.0,
    "ai_estimate": 1075.0,
    "human_adjusted_estimate": 0.0,
    "final_price": 0.0,
    "created_at": "2025-01-16T14:20:00",
    "scheduled_date": "2025-01-21T08:00:00"
  }
]
```

**Status Values**:
- `scheduled` - Job assigned, not started
- `in_progress` - Field worker on site
- `completed` - Work done, awaiting invoice
- `invoiced` - Invoice sent to customer
- `paid` - Customer paid

---

### 3. Get Single Job

**Endpoint**: `GET /api/jobs/{job_id}`

**Purpose**: Get detailed job info including all rooms

**Request**:
```bash
curl https://cleanoutpro.railway.app/api/jobs/1
```

**Response**:
```json
{
  "id": 1,
  "customer_id": 1,
  "address": "123 Main St, Boston MA",
  "status": "in_progress",
  "base_estimate": 450.0,
  "ai_estimate": 675.0,
  "created_at": "2025-01-15T10:30:00",
  "customer": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234"
  },
  "rooms": [
    {
      "id": 1,
      "job_id": 1,
      "room_name": "Master Bedroom",
      "ai_size_class": "large",
      "ai_workload_class": "heavy",
      "ai_confidence": 0.87,
      "estimated_cost": 450.0,
      "image_url": "https://storage.example.com/room1.jpg",
      "created_at": "2025-01-15T11:00:00"
    }
  ]
}
```

---

### 4. Create New Job

**Endpoint**: `POST /api/jobs`

**Purpose**: Create job when field worker arrives at new site

**Request**:
```bash
curl -X POST https://cleanoutpro.railway.app/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "address": "789 Elm St, Somerville MA",
    "status": "in_progress",
    "scheduled_date": "2025-01-22T09:00:00"
  }'
```

**Response**:
```json
{
  "id": 3,
  "customer_id": 1,
  "address": "789 Elm St, Somerville MA",
  "status": "in_progress",
  "base_estimate": 0.0,
  "ai_estimate": 0.0,
  "created_at": "2025-01-17T08:30:00",
  "scheduled_date": "2025-01-22T09:00:00"
}
```

---

### 5. Classify Room (MAIN FEATURE)

**Endpoint**: `POST /api/rooms/classify`

**Purpose**: Upload room photo → Get AI classification + pricing

**Request** (multipart/form-data):
```bash
curl -X POST https://cleanoutpro.railway.app/api/rooms/classify \
  -F "job_id=1" \
  -F "room_name=Master Bedroom" \
  -F "image=@/path/to/photo.jpg"
```

**Request Fields**:
- `job_id` (integer, required): Which job this room belongs to
- `room_name` (string, required): Room description (e.g., "Kitchen", "Garage")
- `image` (file, required): JPEG/PNG photo of the room

**Response**:
```json
{
  "id": 5,
  "job_id": 1,
  "room_name": "Master Bedroom",
  "ai_size_class": "large",
  "ai_workload_class": "heavy",
  "ai_confidence": 0.87,
  "ai_reasoning": "Analysis: Room dimensions approximately 15x12 feet based on furniture scale. High clutter density observed with multiple furniture pieces, boxes, and loose items. Heavy workload due to furniture disassembly required and stair access challenges.",
  "ai_features": {
    "furniture_count": 8,
    "clutter_density": "high",
    "stairs_required": true,
    "hazards": ["heavy_furniture", "narrow_doorway"]
  },
  "estimated_cost": 450.0,
  "final_size_class": "large",
  "final_workload_class": "heavy",
  "image_url": "https://storage.example.com/rooms/5.jpg",
  "created_at": "2025-01-17T09:15:00"
}
```

**Size Classes**:
- `small` - Closet, half bath (1.0x multiplier)
- `medium` - Bedroom, office (1.5x multiplier)
- `large` - Master bedroom, kitchen (2.0x multiplier)
- `extra_large` - Garage, basement (3.0x multiplier)

**Workload Classes**:
- `light` - Minimal items, easy access (1.0x multiplier)
- `moderate` - Normal clutter, standard access (1.3x multiplier)
- `heavy` - High clutter, furniture disassembly (1.6x multiplier)
- `extreme` - Hoarding, hazmat, severe access issues (2.0x multiplier)

**Pricing Formula**:
```
Base Labor: $150
Room Cost = $150 × size_multiplier × workload_multiplier
```

Examples:
- Small + Light: $150 × 1.0 × 1.0 = **$150**
- Medium + Moderate: $150 × 1.5 × 1.3 = **$292.50**
- Large + Heavy: $150 × 2.0 × 1.6 = **$480**
- Extra Large + Extreme: $150 × 3.0 × 2.0 = **$900**

**AI Processing Time**: 10-30 seconds
- **Important**: Show loading indicator!
- LLaVA model processes image server-side
- Uses "Ultrathink" extended reasoning for accuracy

---

### 6. Update Room

**Endpoint**: `PUT /api/rooms/{room_id}`

**Purpose**: Update room details (human override)

**Request**:
```bash
curl -X PUT https://cleanoutpro.railway.app/api/rooms/5 \
  -H "Content-Type: application/json" \
  -d '{
    "room_name": "Master Bedroom (Updated)",
    "human_size_class": "extra_large",
    "human_workload_class": "extreme",
    "human_override_reason": "Hoarding situation worse than AI estimated"
  }'
```

**Response**:
```json
{
  "id": 5,
  "room_name": "Master Bedroom (Updated)",
  "ai_size_class": "large",
  "ai_workload_class": "heavy",
  "human_size_class": "extra_large",
  "human_workload_class": "extreme",
  "human_override_reason": "Hoarding situation worse than AI estimated",
  "final_size_class": "extra_large",
  "final_workload_class": "extreme",
  "estimated_cost": 900.0,
  "created_at": "2025-01-17T09:15:00",
  "updated_at": "2025-01-17T10:30:00"
}
```

**Note**: `final_*` fields = human override if present, else AI classification

---

### 7. List Rooms for Job

**Endpoint**: `GET /api/jobs/{job_id}/rooms`

**Purpose**: Get all rooms already classified for a job

**Request**:
```bash
curl https://cleanoutpro.railway.app/api/jobs/1/rooms
```

**Response**:
```json
[
  {
    "id": 1,
    "room_name": "Master Bedroom",
    "final_size_class": "large",
    "final_workload_class": "heavy",
    "estimated_cost": 450.0,
    "image_url": "https://storage.example.com/room1.jpg"
  },
  {
    "id": 2,
    "room_name": "Kitchen",
    "final_size_class": "large",
    "final_workload_class": "moderate",
    "estimated_cost": 390.0,
    "image_url": "https://storage.example.com/room2.jpg"
  }
]
```

---

### 8. Offline Sync (Future)

**Endpoint**: `POST /api/sync/upload`

**Purpose**: Upload queued operations from offline mobile app

**Request**:
```bash
curl -X POST https://cleanoutpro.railway.app/api/sync/upload \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [
      {
        "type": "create_room",
        "job_id": 1,
        "room_name": "Garage",
        "image_base64": "data:image/jpeg;base64,/9j/4AAQ...",
        "timestamp": "2025-01-17T12:00:00"
      },
      {
        "type": "update_job",
        "job_id": 1,
        "status": "completed",
        "timestamp": "2025-01-17T13:00:00"
      }
    ]
  }'
```

**Response**:
```json
{
  "processed": 2,
  "failed": 0,
  "conflicts": []
}
```

**Note**: Not implemented yet - for offline mode v2

---

## Error Handling

All errors return standard format:

**Format**:
```json
{
  "detail": "Error message here"
}
```

**Common HTTP Status Codes**:
- `200 OK` - Success
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid input (missing fields, wrong format)
- `404 Not Found` - Resource doesn't exist (job_id, room_id)
- `422 Unprocessable Entity` - Validation failed
- `500 Internal Server Error` - Server error (AI processing failed, database error)

**Example Error**:
```json
{
  "detail": "Job with id 999 not found"
}
```

---

## Mobile App Features to Implement

### Phase 1: Core Functionality (MVP)

**Screens**:
1. **Job List** - Show all jobs, tap to select
2. **Job Details** - Show job info + list of rooms already classified
3. **Camera** - Capture room photo
4. **Classification Results** - Show AI results (size, workload, cost)

**User Flow**:
```
1. Open app
2. See list of jobs (GET /api/jobs)
3. Tap job #123
4. See job details (GET /api/jobs/123)
5. Tap "Add Room"
6. Enter room name ("Master Bedroom")
7. Tap "Take Photo" → Camera opens
8. Capture photo
9. Show preview
10. Tap "Submit"
11. Show loading (10-30s)
12. Display results (size, workload, cost)
13. Return to job details (shows new room in list)
```

**Required Libraries**:
```bash
npm install @react-navigation/native @react-navigation/stack
npm install react-native-camera
npm install axios
npm install @reduxjs/toolkit react-redux
```

### Phase 2: Offline Mode

**Features**:
- Local SQLite database for jobs/rooms
- Queue operations when offline
- Sync when back online
- Show sync status indicator

**Libraries**:
```bash
npm install react-native-sqlite-storage
npm install @react-native-community/netinfo
```

### Phase 3: Polish

**Features**:
- Push notifications (job assignments)
- GPS location tagging
- Image compression before upload
- Progress indicators
- Error retry logic

---

## Sample React Native Code

### API Service (`src/services/api.js`)

```javascript
import axios from 'axios';

const API_BASE_URL = 'https://cleanoutpro.railway.app';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for AI processing
  headers: {
    'Content-Type': 'application/json',
  },
});

export const jobsAPI = {
  // Get all jobs
  getJobs: () => api.get('/api/jobs'),

  // Get single job with rooms
  getJob: (jobId) => api.get(`/api/jobs/${jobId}`),

  // Create new job
  createJob: (data) => api.post('/api/jobs', data),

  // Update job status
  updateJob: (jobId, data) => api.put(`/api/jobs/${jobId}`, data),
};

export const roomsAPI = {
  // Classify room with image
  classifyRoom: async (jobId, roomName, imageUri) => {
    const formData = new FormData();
    formData.append('job_id', jobId);
    formData.append('room_name', roomName);
    formData.append('image', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'room.jpg',
    });

    return api.post('/api/rooms/classify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Get rooms for job
  getJobRooms: (jobId) => api.get(`/api/jobs/${jobId}/rooms`),

  // Update room
  updateRoom: (roomId, data) => api.put(`/api/rooms/${roomId}`, data),
};

export default api;
```

### Camera Screen (`src/screens/CameraScreen.js`)

```javascript
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, ActivityIndicator } from 'react-native';
import { RNCamera } from 'react-native-camera';
import { roomsAPI } from '../services/api';

export default function CameraScreen({ route, navigation }) {
  const { jobId, roomName } = route.params;
  const [photo, setPhoto] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const takePicture = async (camera) => {
    const options = { quality: 0.7, base64: false };
    const data = await camera.takePictureAsync(options);
    setPhoto(data.uri);
  };

  const uploadAndClassify = async () => {
    setLoading(true);
    try {
      const response = await roomsAPI.classifyRoom(jobId, roomName, photo);
      setResult(response.data);
    } catch (error) {
      alert('Classification failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <View style={{ flex: 1, padding: 20 }}>
        <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 20 }}>
          ✅ Classification Complete
        </Text>
        <Text>Room: {result.room_name}</Text>
        <Text>Size: {result.final_size_class}</Text>
        <Text>Workload: {result.final_workload_class}</Text>
        <Text style={{ fontSize: 20, fontWeight: 'bold', marginTop: 10 }}>
          Estimate: ${result.estimated_cost.toFixed(2)}
        </Text>
        <TouchableOpacity
          style={{ backgroundColor: '#2563eb', padding: 15, borderRadius: 8, marginTop: 20 }}
          onPress={() => navigation.goBack()}
        >
          <Text style={{ color: 'white', textAlign: 'center' }}>Done</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (photo) {
    return (
      <View style={{ flex: 1, padding: 20 }}>
        <Image source={{ uri: photo }} style={{ flex: 1, borderRadius: 8 }} />
        {loading ? (
          <View style={{ padding: 20 }}>
            <ActivityIndicator size="large" color="#2563eb" />
            <Text style={{ textAlign: 'center', marginTop: 10 }}>
              AI analyzing... (10-30 seconds)
            </Text>
          </View>
        ) : (
          <View style={{ flexDirection: 'row', gap: 10, marginTop: 20 }}>
            <TouchableOpacity
              style={{ flex: 1, backgroundColor: '#6b7280', padding: 15, borderRadius: 8 }}
              onPress={() => setPhoto(null)}
            >
              <Text style={{ color: 'white', textAlign: 'center' }}>Retake</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={{ flex: 1, backgroundColor: '#2563eb', padding: 15, borderRadius: 8 }}
              onPress={uploadAndClassify}
            >
              <Text style={{ color: 'white', textAlign: 'center' }}>Classify</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    );
  }

  return (
    <View style={{ flex: 1 }}>
      <RNCamera
        style={{ flex: 1 }}
        type={RNCamera.Constants.Type.back}
        captureAudio={false}
      >
        {({ camera }) => (
          <View style={{ flex: 1, justifyContent: 'flex-end', padding: 20 }}>
            <TouchableOpacity
              style={{
                backgroundColor: 'white',
                padding: 20,
                borderRadius: 50,
                alignSelf: 'center',
              }}
              onPress={() => takePicture(camera)}
            >
              <Text style={{ fontSize: 18 }}>📷</Text>
            </TouchableOpacity>
          </View>
        )}
      </RNCamera>
    </View>
  );
}
```

---

## Testing Checklist

Before submitting your work, test these scenarios:

**Happy Path**:
- [ ] List jobs successfully
- [ ] Select a job
- [ ] Enter room name
- [ ] Take photo
- [ ] Upload and classify (wait 10-30s)
- [ ] See results: size, workload, cost
- [ ] Return to job list

**Error Handling**:
- [ ] No internet connection (show error)
- [ ] Invalid job_id (show error)
- [ ] Image too large (compress before upload)
- [ ] AI processing timeout (retry option)
- [ ] Empty room name (validation)

**Edge Cases**:
- [ ] Photo preview rotation (iOS landscape bug)
- [ ] Multiple rapid submissions (disable button while loading)
- [ ] App backgrounded during upload (resume on foreground)

---

## Deliverables

When you finish, provide:

1. **Source Code**: GitHub repo with all React Native code
2. **APK/IPA**: Installable builds for testing
3. **Documentation**: README with setup instructions
4. **Demo Video**: 2-minute screen recording showing key features
5. **API Integration**: Proof of successful API calls (screenshots)

---

## Timeline Estimate

**Full-time developer**:
- Phase 1 (MVP): 1-2 weeks
- Phase 2 (Offline): 1 week
- Phase 3 (Polish): 1 week
- **Total**: 3-4 weeks

**Part-time developer**:
- **Total**: 6-8 weeks

---

## Questions?

**Backend API Issues**:
- Check `DEPLOYMENT_STATUS.md` for current deployment status
- Test endpoint: `curl https://your-backend.railway.app/`
- Expected response: `{"message": "CleanoutPro API is running"}`

**AI Processing Slow**:
- Normal: 10-30 seconds per image
- LLaVA model runs server-side (not on phone)
- Always show loading indicator

**Image Upload Fails**:
- Check file size (max 10MB recommended)
- Compress before upload: `quality: 0.7` in camera options
- Ensure HTTPS (iOS blocks HTTP)

**Need Help?**:
- Review `CLAUDE.md` for full project architecture
- Check `API_QUICKSTART.md` for more API examples
- Test API endpoints with Postman first

---

## Success Criteria

Your app is ready when:
1. ✅ Field worker can select a job
2. ✅ Capture room photo with camera
3. ✅ Photo uploads successfully
4. ✅ AI returns classification (10-30s)
5. ✅ Results display clearly: Room, Size, Workload, Cost
6. ✅ App handles errors gracefully
7. ✅ Works on iOS and Android
8. ✅ Builds install without crashes

**Good luck building!** 🚀
