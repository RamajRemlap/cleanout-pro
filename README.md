# CleanoutPro - Cleanout Business Management System

**AI-powered cleanout/junk removal business management with mobile capture, desktop control, and automated invoicing.**

## 🎯 Core Principle

**"If visualization breaks, business must still run"** - The 3D cube is enhancement, not dependency.

## 🏗️ Architecture

Three-part system:
1. **Mobile Capture** (React Native) - Room photos → AI classification → Estimates
2. **Desktop Control** (Electron + React) - 3D cube viz + Adjustments + Invoicing + PayPal
3. **Cloud Backend** (FastAPI + PostgreSQL) - AI processing + Data + Real-time sync

## 🚀 Quick Start

### Prerequisites

- ✅ Python 3.8+ (Installed)
- ✅ Node.js 18+ (Installed: v22.16.0)
- ✅ Ollama (Installed)
- ⬜ Docker Desktop (for PostgreSQL + Redis)
- ⬜ LLaVA vision model

### 1. Install LLaVA Vision Model

```bash
ollama pull llava:7b
```

### 2. Start Databases (Docker)

```bash
cd cleanout-pro
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- Automatically loads database schema

### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env with your PayPal credentials

# Run backend
python api/main.py
```

Backend runs at: http://localhost:8000

API docs at: http://localhost:8000/docs

### 4. Test AI Classification

```bash
# In Python shell
from services.ai_vision import get_ai_vision_service

ai = get_ai_vision_service()

# Test connection
print(ai.test_connection())  # Should print True

# Test model
print(ai.check_model_installed())  # Should print True

# Classify an image
with open('test_room.jpg', 'rb') as f:
    image_data = f.read()
    result = ai.classify_room(image_data, room_name="Test Room")
    print(result)
```

## 📁 Project Structure

```
cleanout-pro/
├── backend/                   # FastAPI Backend
│   ├── api/
│   │   ├── main.py           # ✅ FastAPI entry point
│   │   └── routes/           # API endpoints (TODO)
│   ├── database/
│   │   ├── schemas.sql       # ✅ PostgreSQL schema
│   │   └── models.py         # SQLAlchemy ORM (TODO)
│   ├── services/
│   │   ├── ai_vision.py      # ✅ Ollama LLaVA + Ultrathink
│   │   ├── pricing_engine.py # ✅ Cost calculation
│   │   └── paypal_service.py # PayPal integration (TODO)
│   └── requirements.txt      # ✅ Python dependencies
│
├── mobile/                    # React Native App (TODO)
├── desktop/                   # Electron + React (TODO)
└── docker-compose.yml        # ✅ PostgreSQL + Redis
```

## 🤖 AI Vision (Ultrathink)

The system uses **Ollama LLaVA** with extended reasoning for accurate room classification:

**What it analyzes:**
- Room size (small, medium, large, extra_large)
- Workload difficulty (light, moderate, heavy, extreme)
- Clutter density (0.0 to 1.0)
- Accessibility (easy, moderate, difficult)
- Item categories (furniture, boxes, appliances, etc.)
- Salvage potential (none, low, medium, high)

**Ultrathink mode:**
- Step-by-step reasoning
- Confidence scoring
- Detailed feature detection

## 💰 Pricing System

**Base Formula:**
```
Room Cost = Base Labor × Size Multiplier × Workload Multiplier + Adjustments
```

**Default Rates:**
- Base Labor: $150.00
- Small room: 1.0x
- Medium room: 1.5x
- Large room: 2.0x
- Extra large: 3.0x

**Workload Multipliers:**
- Light: 1.0x
- Moderate: 1.3x
- Heavy: 1.6x
- Extreme: 2.0x

**Adjustments:**
- Bin rental (20-yard): +$200
- Bin rental (30-yard): +$300
- Stairs (per flight): +$25
- Difficult access: +$75
- Hazmat handling: +$150

## 🔐 Critical Implementation Rules

### 1. Plain Invoices (No AI Jargon)

**✅ GOOD:**
```
Master Bedroom Cleanout - $450.00
Garage Cleanout - $600.00
```

**❌ BAD:**
```
Master Bedroom (AI: Large/Heavy, 87%) - $450.00
```

### 2. Human Overrides AI

- Desktop adjustments are **authoritative**
- AI classification preserved for audit
- Pricing recalculates on human override

### 3. Visualization is Enhancement

- Cube can break, business continues
- Always provide table fallback
- All operations work from table view

### 4. Filter: "See, Decide, or Get Paid?"

Every feature must help:
- **See:** Visualize job status
- **Decide:** Make better estimates
- **Get Paid:** Generate invoices/collect payment

## 💳 PayPal Setup

1. Go to https://developer.paypal.com
2. Create sandbox app
3. Get Client ID & Secret
4. Create webhook
5. Update `.env` file

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=. --cov-report=html
```

## 📊 Database Schema

**Core tables:**
- `customers` - Customer information
- `jobs` - Job tracking
- `rooms` - Room captures + AI classification
- `invoices` - Invoice generation
- `payment_transactions` - PayPal payments
- `pricing_rules` - Configurable pricing
- `sync_queue` - Mobile offline sync

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f backend

# Rebuild after changes
docker-compose up --build
```

## 🌐 Deployment (FREE Options)

**Backend:** Railway.app (free tier)
**Database:** Neon (free PostgreSQL)
**Redis:** Upstash (free tier)
**Storage:** Cloudinary (free tier)
**Cost:** $0/month

See full deployment guide in `/docs/deployment.md`

## 📈 Development Roadmap

- ✅ **Phase 1 (Weeks 1-2):** Backend foundation
- ⬜ **Phase 2 (Weeks 3-4):** Mobile app
- ⬜ **Phase 3 (Weeks 5-6):** Desktop app + Cube
- ⬜ **Phase 4 (Week 7):** Pricing & Invoices
- ⬜ **Phase 5 (Week 8):** PayPal integration
- ⬜ **Phase 6 (Week 9):** Real-time sync
- ⬜ **Phase 7 (Week 10):** Testing
- ⬜ **Phase 8 (Week 11):** Deployment
- ⬜ **Phase 9 (Week 12):** Documentation

## 🤝 Contributing

This is a complete business system. Follow the plan in `/docs/implementation-plan.md`

## 📄 License

Proprietary - CleanoutPro Business System

## 🆘 Troubleshooting

**LLaVA not found:**
```bash
ollama pull llava:7b
ollama list  # Verify installation
```

**Database connection error:**
```bash
docker-compose ps  # Check if PostgreSQL is running
docker-compose logs postgres  # View logs
```

**Ollama not responding:**
```bash
ollama serve  # Start Ollama service
```

## 📞 Support

Check `/docs/troubleshooting.md` for common issues.

---

**Built with:**
- FastAPI (Backend)
- React Native (Mobile)
- Electron + React (Desktop)
- Ollama LLaVA (AI Vision)
- PostgreSQL (Database)
- PayPal (Payments)
