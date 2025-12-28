# CleanoutPro Quick Start Guide

**Status**: All components built! Follow these steps to get your system running.

## 🎯 What You Have

✅ **Mobile App** - React Native app with camera capture
✅ **Backend API** - FastAPI with AI vision integration
✅ **Desktop App** - Electron app for office staff
✅ **Lead Generator** - Michigan job finder (Facebook + Craigslist)
✅ **Ollama + LLaVA** - AI vision model (downloading: 36% complete)

## 🚀 Quick Start (5 Minutes)

### Step 1: Start Backend API

```bash
# Navigate to backend
cd backend

# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies (if not done)
pip install -r requirements.txt

# Start backend server
python api/main.py
```

Backend will run at: **http://localhost:8000**

Test it: Open http://localhost:8000/docs in your browser

### Step 2: Start Mobile App (Field Workers)

```bash
# Open new terminal
cd mobile

# Install dependencies
npm install

# Start Metro bundler
npm start

# In another terminal, run:
npm run android  # For Android
# npm run ios     # For iOS
```

### Step 3: Start Desktop App (Office Staff)

```bash
# Open new terminal
cd desktop

# Install dependencies
npm install

# Start desktop app
npm start
```

## 📱 Mobile App Usage Flow

1. **Open app** → See list of jobs
2. **Select job** → View rooms for that job
3. **Tap "Add Room"** → Camera opens
4. **Capture photo** → Frame room in guide
5. **Enter room name** → e.g., "Master Bedroom"
6. **Upload** → Photo sent to backend
7. **AI analyzes** → Returns size, workload, estimate
8. **View results** → See classification + confidence

## 🔍 Finding Jobs (Michigan Lead Generator)

```bash
cd backend

# Run lead generator
python services/michigan_lead_generator.py
```

This will:
- Scrape Facebook Marketplace and Craigslist
- Find cleanout/junk removal leads in 30+ Michigan cities
- Store in `michigan_leads.db`
- Prioritize by urgency score and estimated value

View leads:
```bash
sqlite3 michigan_leads.db "SELECT * FROM leads WHERE urgency_score >= 0.6 ORDER BY urgency_score DESC LIMIT 10;"
```

## 🤖 AI Vision Setup

**Status**: LLaVA model is downloading (36% complete, ~3.5 hours remaining)

Once download completes, test AI:

```bash
# Check Ollama is running
ollama list

# Test AI vision
cd backend
python -c "from services.ai_vision import get_ai_vision_service; print(get_ai_vision_service().test_connection())"
```

**Note**: Until LLaVA finishes downloading, the backend will return default classifications (medium/moderate) with 0.0 confidence.

## 🗄️ Database Setup

Your backend uses **Neon.tech PostgreSQL** (cloud database).

Check `backend/.env` for `DATABASE_URL`.

To create tables:
```bash
cd backend
python -c "from database.connection import engine; from database.models import Base; Base.metadata.create_all(engine)"
```

## 🧪 Testing End-to-End Flow

### Test 1: Backend Health

```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

### Test 2: Create Test Job

```bash
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "00000000-0000-0000-0000-000000000000",
    "job_number": "TEST001",
    "status": "scheduled"
  }'
```

### Test 3: Upload Room Photo (from mobile app)

1. Open mobile app
2. Select test job
3. Tap "Add Room"
4. Capture/select photo
5. Name it "Test Room"
6. Upload

Backend will:
- Save image to `backend/uploads/rooms/`
- Call Ollama LLaVA for classification
- Return estimate

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     CleanoutPro System                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📱 Mobile App (React Native)                               │
│  └─ Field workers capture room photos                      │
│  └─ Photos → Backend API                                   │
│                                                              │
│  🖥️ Desktop App (Electron)                                  │
│  └─ Office staff review estimates                          │
│  └─ 3D visualization + table view                          │
│  └─ Generate invoices, process payments                    │
│                                                              │
│  ⚡ Backend API (FastAPI + Python)                          │
│  └─ POST /api/rooms → Upload photo                         │
│  └─ Ollama LLaVA → AI classification                       │
│  └─ Pricing engine → Calculate estimate                    │
│  └─ PostgreSQL → Store data                                │
│                                                              │
│  🔍 Lead Generator                                          │
│  └─ Scrape Facebook + Craigslist                           │
│  └─ Find Michigan cleanout jobs                            │
│  └─ Prioritize by urgency                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Troubleshooting

### Backend won't start

```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install --upgrade -r backend/requirements.txt

# Check .env file exists
ls backend/.env
```

### Mobile app can't connect to backend

Update `mobile/.env`:

```env
# For Android emulator
API_URL=http://10.0.2.2:8000

# For iOS simulator
API_URL=http://localhost:8000

# For physical device (use your computer's IP)
API_URL=http://192.168.1.XXX:8000
```

### AI classification not working

Check if:
1. Ollama is running: `ollama list`
2. LLaVA model installed: Should see `llava:7b` in list
3. Backend can reach Ollama: Check `backend/.env` has `OLLAMA_URL=http://localhost:11434`

### No jobs showing in mobile app

1. Create test data:
```bash
cd backend
python create_test_data.py
```

2. Or create via API:
```bash
curl -X POST http://localhost:8000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Customer", "phone": "555-1234", "address": "123 Main St"}'
```

## 📞 Next Steps

1. **Wait for LLaVA download** to complete for full AI vision
2. **Run lead generator** to find Michigan jobs
3. **Test mobile app** by capturing a room photo
4. **Review in desktop app** and adjust estimates
5. **Generate invoice** and collect payment

## 🎓 Learning Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Native**: https://reactnative.dev
- **Ollama**: https://ollama.ai
- **Neon Database**: https://neon.tech

---

**Need Help?** Check the detailed README files:
- `backend/README.md` - Backend API guide
- `mobile/README.md` - Mobile app guide
- `desktop/README.md` - Desktop app guide
