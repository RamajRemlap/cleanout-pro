# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CleanoutPro is an AI-powered cleanout/junk removal business management system with three components:
1. **Mobile app (React Native)**: Field workers capture room photos → AI classifies → Generates estimates
2. **Desktop app (Electron + React)**: Office staff view 3D visualization, adjust estimates, generate invoices, process PayPal payments
3. **Backend API (FastAPI + Python)**: AI processing via Ollama LLaVA, database operations, real-time sync

**Core Principle**: "If visualization breaks, business must still run" - The 3D cube is an enhancement, not a dependency. All operations must work from table view fallback.

## Development Commands

### Backend (FastAPI + Python)

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run development server (port 8000)
python api/main.py

# Or with uvicorn directly (port 8001)
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload

# Run tests
pytest
pytest --cov=. --cov-report=html

# Test AI vision service (requires Ollama + LLaVA)
python -c "from services.ai_vision import get_ai_vision_service; print(get_ai_vision_service().test_connection())"
```

### Database Setup

**Option 1: Neon.tech (Recommended for development)**
- Uses cloud PostgreSQL (already configured)
- Connection string in `backend/.env` as `DATABASE_URL`
- Schema auto-created via `backend/database/schemas.sql`

**Option 2: Local PostgreSQL**
```bash
# Install PostgreSQL locally, then:
createdb cleanoutpro
psql -U postgres -d cleanoutpro -f backend/database/schemas.sql
```

**Option 3: Docker Compose**
```bash
# Start all services (PostgreSQL + Redis + Backend)
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Rebuild after changes
docker-compose up --build
```

### Prerequisites

Required services:
- **Ollama** (http://localhost:11434): AI vision model host
- **LLaVA model**: `ollama pull llava:7b`
- **PostgreSQL**: Database (Neon cloud or local)
- **Redis**: Caching layer (optional for development)

## Architecture

### Data Flow: Mobile → AI → Desktop → Invoice

1. **Mobile captures room photo** → Uploads to backend `/api/rooms/classify`
2. **Backend AI processing**:
   - `services/ai_vision.py`: Ollama LLaVA analyzes image using "Ultrathink" extended reasoning
   - Returns: `size_class` (small/medium/large/extra_large), `workload_class` (light/moderate/heavy/extreme), confidence score, reasoning chain
   - Stores in `rooms` table: `ai_size_class`, `ai_workload_class`, `ai_confidence`, `ai_reasoning`
3. **Pricing calculation**:
   - `services/pricing_engine.py`: Applies multipliers from `pricing_rules` table
   - Formula: `base_labor ($150) × size_multiplier × workload_multiplier + adjustments`
   - Stores in `rooms.estimated_cost` and `jobs.ai_estimate`
4. **Desktop review**:
   - Human can override AI classification → `rooms.human_size_class`, `rooms.human_workload_class`
   - Final classification: `rooms.final_size_class` = human override OR AI classification
5. **Invoice generation**:
   - `pricing_engine.generate_invoice_line_items()`: **NO AI JARGON** - plain descriptions only
   - ✅ GOOD: "Master Bedroom Cleanout - $450.00"
   - ❌ BAD: "Master Bedroom (AI: Large/Heavy, 87%) - $450.00"

### Database Schema (PostgreSQL)

**Core entities**:
- `customers` → `jobs` → `rooms` (one-to-many relationships)
- `jobs` → `invoices` → `payment_transactions`
- `pricing_rules`: Configurable multipliers and flat fees
- `sync_queue`: Mobile offline sync operations
- `audit_log`: All human overrides and changes

**Key fields in `rooms` table**:
- AI classification: `ai_size_class`, `ai_workload_class`, `ai_confidence`, `ai_reasoning`, `ai_features` (JSONB)
- Human overrides: `human_size_class`, `human_workload_class`, `human_override_reason`
- **Final authority**: `final_size_class`, `final_workload_class` (used for pricing)

**Jobs pricing fields**:
- `base_estimate`: Sum of all room costs (AI-only)
- `ai_estimate`: Base + job-level adjustments (stairs, bin rental)
- `human_adjusted_estimate`: After desktop overrides
- `final_price`: What customer pays (must match invoice total)

### AI Vision Service (`services/ai_vision.py`)

**Ultrathink Mode**: Extended chain-of-thought reasoning for higher accuracy
- Analyzes room dimensions, clutter density, item types, accessibility, hazards
- Returns structured JSON with confidence scores
- Fallback: If AI fails, returns `medium/moderate` with 0.0 confidence

**Important**: AI classification is **preserved for audit**, but human override is **authoritative**. Pricing engine always uses `final_*` fields.

### Pricing Engine (`services/pricing_engine.py`)

**Multipliers** (from `pricing_rules` table or defaults):
```python
SIZE_MULTIPLIERS = {
    'small': 1.0,
    'medium': 1.5,
    'large': 2.0,
    'extra_large': 3.0
}

WORKLOAD_MULTIPLIERS = {
    'light': 1.0,
    'moderate': 1.3,
    'heavy': 1.6,
    'extreme': 2.0
}
```

**Adjustments** (flat fees):
- Bin rental (20-yard): +$200
- Bin rental (30-yard): +$300
- Stairs (per flight): +$25
- Difficult access: +$75
- Hazmat handling: +$150

**Critical rule**: Invoice line items must be **plain English**, never expose AI classification details to customers.

## Critical Implementation Rules

### 1. Human Overrides AI
- Desktop adjustments are **final authority**
- AI classification is **preserved** in `ai_*` fields for audit trail
- Pricing uses `final_*` fields (human override OR AI if no override)
- Never delete AI data when human overrides - both coexist

### 2. Plain Invoices (No AI Jargon)
Customers must never see AI terminology in invoices:
```python
# ✅ GOOD
"Master Bedroom Cleanout - $450.00"

# ❌ BAD
"Master Bedroom (AI: Large/Heavy, 87% confidence) - $450.00"
```

### 3. Visualization is Enhancement, Not Dependency
- 3D cube can break, business continues
- Every feature in desktop app needs table view fallback
- All CRUD operations must work without visualization
- Filter features by: "See, Decide, or Get Paid?"
  - **See**: Visualize job status
  - **Decide**: Make better estimates
  - **Get Paid**: Generate invoices/collect payment

### 4. Database is Source of Truth
- Mobile app can work offline (uses `sync_queue`)
- Desktop reads directly from database
- Real-time sync via WebSocket when online
- Conflict resolution: Last write wins (with audit log)

## File Structure

```
cleanout-pro/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI entry point, CORS, health checks
│   │   └── routes/
│   │       ├── jobs.py          # Job CRUD endpoints
│   │       └── rooms.py         # Room classification + image upload
│   ├── database/
│   │   ├── connection.py        # SQLAlchemy engine, session factory
│   │   ├── models.py            # ORM models (Customer, Job, Room, Invoice, etc.)
│   │   └── schemas.sql          # PostgreSQL schema with triggers
│   ├── services/
│   │   ├── ai_vision.py         # Ollama LLaVA integration with Ultrathink
│   │   └── pricing_engine.py   # Cost calculation with multipliers
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Template for environment variables
│   └── create_test_data.py      # Seed database with sample data
├── mobile/                       # React Native (TODO)
├── desktop/                      # Electron + React (TODO)
├── docker-compose.yml            # PostgreSQL + Redis + Backend containers
└── README.md                     # User-facing documentation
```

## Environment Variables

Required in `backend/.env`:
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/cleanoutpro

# Ollama (AI Vision)
OLLAMA_URL=http://localhost:11434

# Redis (optional for development)
REDIS_URL=redis://localhost:6379

# PayPal (production)
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_SECRET=your_secret
PAYPAL_MODE=sandbox  # or 'live'

# App settings
APP_URL=http://localhost:3000
```

## Testing Notes

When testing AI vision:
1. Ensure Ollama is running: `ollama serve`
2. Verify LLaVA model installed: `ollama list`
3. Test connection before classification
4. AI can be slow (10-30s per image) - use async processing
5. Always provide fallback UI while processing

When testing pricing:
1. Check `pricing_rules` table for current multipliers
2. Verify calculation: `base ($150) × size × workload + adjustments`
3. Test human override flow: AI classification → human adjustment → recalculation
4. Ensure invoice line items are plain language

## PayPal Integration

**Sandbox testing**:
1. Create app at https://developer.paypal.com
2. Use sandbox credentials in `.env`
3. Test with PayPal sandbox accounts
4. Webhook URL: `{APP_URL}/api/paypal/webhook`

**Invoice flow**:
1. Generate invoice → POST `/api/invoices`
2. Create PayPal payment → Returns payment URL
3. Customer pays via PayPal
4. Webhook confirms payment → Update `invoices.status` to 'paid'
5. Record in `payment_transactions` table

## Common Patterns

### Adding a new API endpoint
1. Create route in `backend/api/routes/`
2. Import and register in `api/main.py`
3. Use `Depends(get_db)` for database session
4. Follow FastAPI conventions (Pydantic models for validation)

### Adding a new pricing rule
1. Insert into `pricing_rules` table with `rule_type`
2. Set `active=true` and `priority` for ordering
3. Pricing engine will auto-load on next calculation

### Mobile offline sync
1. Mobile stores operations in local queue
2. When online, POST to `/api/sync/upload`
3. Backend processes `sync_queue` table
4. Returns conflicts for resolution (if any)

## Deployment

**Free tier stack**:
- Backend: Railway.app or Render.com
- Database: Neon.tech (PostgreSQL)
- Redis: Upstash.com
- Storage: Cloudinary (images)
- Cost: $0/month for MVP

See `/docs/deployment.md` for full deployment guide.
