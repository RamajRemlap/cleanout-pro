# CleanoutPro System Overview

**Version**: 1.0.0
**Last Updated**: December 2025
**Status**: Backend Production Ready | Mobile & Desktop In Development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Database Schema](#database-schema)
7. [AI Integration](#ai-integration)
8. [API Structure](#api-structure)
9. [Pricing Engine](#pricing-engine)
10. [Current Implementation Status](#current-implementation-status)
11. [Deployment Architecture](#deployment-architecture)
12. [Security Considerations](#security-considerations)
13. [Future Roadmap](#future-roadmap)

---

## Executive Summary

### What is CleanoutPro?

CleanoutPro is an **AI-powered junk removal business management system** designed to streamline the estimation and invoicing process for cleanout/junk removal companies.

### Core Problem Solved

Traditional junk removal businesses struggle with:
- **Inconsistent pricing** - Manual estimates vary by worker experience
- **Slow quote turnaround** - Customers wait hours/days for estimates
- **Pricing disputes** - Subjective assessments lead to customer complaints
- **Lost revenue** - Under-estimating costs due to missed complexities

### CleanoutPro Solution

**AI-powered room classification** that provides:
- ✅ **Instant estimates** - 10-30 second AI analysis vs hours of manual work
- ✅ **Consistent pricing** - Standardized classification across all workers
- ✅ **Audit trail** - AI reasoning preserved for quality control
- ✅ **Human oversight** - Office staff can review and override AI decisions
- ✅ **Customer transparency** - Photo evidence supports pricing

### Key Business Metrics

- **Estimation time**: 10-30 seconds (vs 2-4 hours manual)
- **Pricing consistency**: 87%+ AI confidence scores
- **Revenue protection**: Captures hidden complexity (stairs, access, hazards)
- **Customer satisfaction**: Visual evidence reduces disputes

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FIELD OPERATIONS                        │
│                                                              │
│  ┌────────────────────────────────────────────┐            │
│  │   Mobile App (React Native)                │            │
│  │   - iOS & Android                          │            │
│  │   - Camera capture                         │            │
│  │   - Offline-first                          │            │
│  │   - GPS location                           │            │
│  └──────────────┬─────────────────────────────┘            │
│                 │                                            │
└─────────────────┼────────────────────────────────────────────┘
                  │
                  │ HTTPS/REST
                  │ (photos, metadata)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND API                             │
│                                                              │
│  ┌────────────────────────────────────────────┐            │
│  │   FastAPI (Python)                         │            │
│  │   - REST endpoints                         │            │
│  │   - Image processing                       │            │
│  │   - Business logic                         │            │
│  │   - WebSocket sync                         │            │
│  └──────┬──────────────────┬──────────────────┘            │
│         │                  │                                │
│         ▼                  ▼                                │
│  ┌─────────────┐    ┌─────────────┐                       │
│  │   Ollama    │    │ PostgreSQL  │                       │
│  │   LLaVA     │    │   Database  │                       │
│  │   (AI)      │    │   (Neon)    │                       │
│  └─────────────┘    └─────────────┘                       │
│                                                              │
└─────────────────┼────────────────────────────────────────────┘
                  │
                  │ HTTPS/REST
                  │ (job data, estimates)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     OFFICE OPERATIONS                       │
│                                                              │
│  ┌────────────────────────────────────────────┐            │
│  │   Desktop App (Electron + React)           │            │
│  │   - 3D visualization                       │            │
│  │   - Estimate review                        │            │
│  │   - Invoice generation                     │            │
│  │   - PayPal integration                     │            │
│  └────────────────────────────────────────────┘            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Three-Tier Architecture

**Tier 1: Presentation Layer**
- **Mobile App** (React Native) - Field workers
- **Desktop App** (Electron + React) - Office staff
- **Mobile Web** (PWA) - Temporary solution for testing

**Tier 2: Application Layer**
- **Backend API** (FastAPI/Python) - Business logic
- **AI Vision Service** (Ollama LLaVA) - Image classification
- **Pricing Engine** (Python) - Cost calculation

**Tier 3: Data Layer**
- **PostgreSQL** (Neon.tech) - Persistent storage
- **Redis** (Upstash) - Caching layer (optional)
- **Cloud Storage** (Cloudinary) - Image storage

---

## Technology Stack

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API Framework** | FastAPI 0.100+ | High-performance REST API |
| **Language** | Python 3.11+ | Backend logic |
| **ORM** | SQLAlchemy 2.0 | Database abstraction |
| **Validation** | Pydantic | Request/response validation |
| **AI Model Host** | Ollama | Local LLM server |
| **AI Model** | LLaVA 7B | Vision-language model |
| **Image Processing** | Pillow | Image manipulation |
| **Database** | PostgreSQL 15+ | Relational data storage |
| **Caching** | Redis (optional) | Performance optimization |

### Mobile (React Native)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | React Native 0.71+ | Cross-platform mobile |
| **Language** | TypeScript | Type-safe development |
| **State Management** | Redux Toolkit / Zustand | App state |
| **Navigation** | React Navigation v6 | Screen routing |
| **Camera** | react-native-camera | Photo capture |
| **Offline Storage** | SQLite / AsyncStorage | Local data persistence |
| **HTTP Client** | Axios | API communication |
| **Location** | react-native-geolocation | GPS tracking |

### Desktop (Electron + React)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Electron 25+ | Cross-platform desktop |
| **UI Library** | React 18+ | User interface |
| **Language** | TypeScript | Type-safe development |
| **3D Rendering** | Three.js | Job visualization |
| **State Management** | Redux Toolkit | App state |
| **Payment** | PayPal SDK | Payment processing |
| **PDF Generation** | PDFKit / jsPDF | Invoice creation |

### Mobile Web (PWA - Temporary)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Vanilla HTML/JS | Lightweight, no build |
| **Service Worker** | Workbox | Offline caching |
| **Manifest** | Web App Manifest | Home screen install |
| **Camera** | HTML5 Media API | Photo capture |
| **Styling** | CSS3 | Responsive design |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Hosting** | Railway / Render | Serverless deployment |
| **Database** | Neon.tech | Managed PostgreSQL |
| **Redis** | Upstash | Managed Redis |
| **Image Storage** | Cloudinary | CDN + processing |
| **Domain/SSL** | Cloudflare | DNS + SSL termination |
| **CI/CD** | GitHub Actions | Automated deployment |

---

## Core Components

### 1. Mobile App (Field Workers)

**Purpose**: Capture room photos on-site and get instant AI estimates

**Key Features**:
- 📷 **Camera Integration**: Native camera access with preview
- 🔄 **Offline Mode**: Work without internet, sync later
- 📍 **GPS Tagging**: Auto-capture job location
- 📊 **AI Results**: Real-time classification display
- ✅ **Simple UX**: Minimal UI for field efficiency

**User Flow**:
1. Field worker arrives at job site
2. Opens app → Selects job (or creates new)
3. Enters room name (e.g., "Master Bedroom")
4. Takes photo of room
5. Taps "Classify" → AI processes (10-30s)
6. Views results: Size, Workload, Cost
7. Repeats for all rooms
8. Submits job for office review

**Data Stored Locally** (for offline):
- Job list (ID, address, status)
- Room photos (base64 or file path)
- Pending upload queue
- User preferences

**Sync Strategy**:
- **Online**: Immediate upload after each photo
- **Offline**: Queue operations, sync when connected
- **Conflict Resolution**: Last write wins (server timestamp)

### 2. Desktop App (Office Staff)

**Purpose**: Review AI estimates, adjust pricing, generate invoices

**Key Features**:
- 🎨 **3D Visualization**: Interactive cube showing job layout
- 📊 **Table View Fallback**: All features work without 3D
- 🤖 **AI Override**: Human can adjust classifications
- 💵 **Invoice Generator**: PDF creation with line items
- 💳 **PayPal Integration**: Direct payment processing
- 📈 **Reporting**: Job analytics and pricing trends

**Critical Rule**: "If visualization breaks, business must still run"
- All CRUD operations accessible via table view
- 3D cube is enhancement, not dependency
- Every feature passes "See, Decide, or Get Paid?" test

**User Flow**:
1. Office staff receives completed job
2. Opens desktop app → Views job in 3D (or table)
3. Reviews AI classifications for each room
4. Adjusts if needed (e.g., AI said "medium", human says "large")
5. Adds job-level adjustments (stairs, bin rental, etc.)
6. Generates invoice (plain language, no AI jargon)
7. Sends to customer via PayPal
8. Marks job as invoiced/paid

### 3. Backend API

**Purpose**: Central hub for business logic, AI processing, data storage

**Responsibilities**:
- 🔌 **REST API**: CRUD operations for jobs, rooms, customers
- 🤖 **AI Orchestration**: Send images to Ollama, process results
- 💰 **Pricing Calculation**: Apply multipliers and adjustments
- 💾 **Data Persistence**: Save to PostgreSQL
- 🔄 **Real-time Sync**: WebSocket for live updates
- 🔐 **Authentication**: JWT tokens (future)
- 📝 **Audit Logging**: Track all changes

**Architecture Pattern**: Service-oriented
- `api/routes/`: HTTP endpoint handlers
- `services/`: Business logic (AI, pricing, sync)
- `database/`: ORM models and schema
- `utils/`: Helper functions

### 4. AI Vision Service

**Purpose**: Analyze room photos and classify size/workload

**Technology**: Ollama LLaVA 7B (vision-language model)

**Input**:
- Room photo (JPEG/PNG)
- Optional context (room name, notes)

**Output**:
```json
{
  "size_class": "large",
  "workload_class": "heavy",
  "confidence": 0.87,
  "reasoning": "Analysis: Room dimensions approximately 15x12 feet...",
  "features": {
    "furniture_count": 8,
    "clutter_density": "high",
    "stairs_required": true,
    "hazards": ["heavy_furniture", "narrow_doorway"]
  }
}
```

**Processing Mode**: "Ultrathink" extended reasoning
- Analyzes room dimensions, clutter, accessibility
- Identifies hazards and special requirements
- Provides confidence score (0.0-1.0)
- Returns reasoning chain for transparency

**Fallback**: If AI fails → Returns `medium/moderate` with 0.0 confidence

### 5. Pricing Engine

**Purpose**: Calculate job costs based on classifications

**Formula**:
```
Base Labor: $150 per room

Room Cost = $150 × size_multiplier × workload_multiplier

Job Total = Sum(all rooms) + adjustments
```

**Multipliers** (configurable via `pricing_rules` table):

| Size Class | Multiplier | Example Rooms |
|------------|-----------|---------------|
| Small | 1.0x | Closet, half bath |
| Medium | 1.5x | Bedroom, office |
| Large | 2.0x | Master bedroom, kitchen |
| Extra Large | 3.0x | Garage, basement, attic |

| Workload Class | Multiplier | Description |
|----------------|-----------|-------------|
| Light | 1.0x | Minimal items, easy access |
| Moderate | 1.3x | Normal clutter, standard access |
| Heavy | 1.6x | High clutter, furniture disassembly |
| Extreme | 2.0x | Hoarding, hazmat, severe access |

**Job-Level Adjustments** (flat fees):
- Bin rental (20-yard): +$200
- Bin rental (30-yard): +$300
- Stairs (per flight): +$25
- Difficult access: +$75
- Hazmat handling: +$150

**Example Calculations**:
```
Small Closet (Light):
$150 × 1.0 × 1.0 = $150

Medium Bedroom (Moderate):
$150 × 1.5 × 1.3 = $292.50

Large Garage (Heavy):
$150 × 2.0 × 1.6 = $480

Extra Large Basement (Extreme):
$150 × 3.0 × 2.0 = $900

Job with 3 rooms + stairs (2 flights):
$450 (rooms) + $50 (stairs) = $500
```

---

## Data Flow

### End-to-End Job Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. JOB CREATION                                             │
└─────────────────────────────────────────────────────────────┘
   Mobile App → POST /api/jobs
   {
     "customer_id": 1,
     "address": "123 Main St",
     "status": "scheduled"
   }
   ↓
   Database: Insert into `jobs` table
   ↓
   Return: Job ID #123

┌─────────────────────────────────────────────────────────────┐
│ 2. ROOM CAPTURE & CLASSIFICATION                           │
└─────────────────────────────────────────────────────────────┘
   Mobile App → POST /api/rooms/classify
   FormData:
     - job_id: 123
     - room_name: "Master Bedroom"
     - image: [photo.jpg]
   ↓
   Backend API:
     1. Save image to storage → Get URL
     2. Send to AI Vision Service (Ollama)
     3. AI processes (10-30 seconds)
        - Analyzes dimensions, clutter, hazards
        - Returns size/workload classification
     4. Pricing Engine calculates cost
        - $150 × size × workload
     5. Save to database
   ↓
   Database: Insert into `rooms` table
   {
     "job_id": 123,
     "room_name": "Master Bedroom",
     "ai_size_class": "large",
     "ai_workload_class": "heavy",
     "ai_confidence": 0.87,
     "ai_reasoning": "...",
     "estimated_cost": 480.00,
     "image_url": "https://..."
   }
   ↓
   Return: Classification results to mobile app

┌─────────────────────────────────────────────────────────────┐
│ 3. OFFICE REVIEW & ADJUSTMENT                              │
└─────────────────────────────────────────────────────────────┘
   Desktop App → GET /api/jobs/123
   ↓
   Display: All rooms with AI classifications
   ↓
   Human Review:
     - AI said "large/heavy" ($480)
     - Actually "extra_large/extreme" (worse than expected)
   ↓
   Desktop App → PUT /api/rooms/5
   {
     "human_size_class": "extra_large",
     "human_workload_class": "extreme",
     "human_override_reason": "Hoarding situation"
   }
   ↓
   Pricing Engine: Recalculate
     - $150 × 3.0 × 2.0 = $900
   ↓
   Database: Update `rooms` table
   {
     "ai_size_class": "large",        ← Preserved for audit
     "ai_workload_class": "heavy",    ← Preserved for audit
     "human_size_class": "extra_large",
     "human_workload_class": "extreme",
     "final_size_class": "extra_large",    ← Used for pricing
     "final_workload_class": "extreme",     ← Used for pricing
     "estimated_cost": 900.00
   }

┌─────────────────────────────────────────────────────────────┐
│ 4. INVOICE GENERATION                                      │
└─────────────────────────────────────────────────────────────┘
   Desktop App → POST /api/invoices
   {
     "job_id": 123,
     "adjustments": [
       {"type": "stairs", "quantity": 2, "cost": 50},
       {"type": "bin_rental_20", "quantity": 1, "cost": 200}
     ]
   }
   ↓
   Pricing Engine: Generate line items
     ✅ GOOD: "Master Bedroom Cleanout - $900.00"
     ✅ GOOD: "Stair Access (2 flights) - $50.00"
     ✅ GOOD: "Bin Rental (20-yard) - $200.00"
     ❌ BAD: "Master Bedroom (AI: Large/Heavy 87%) - $900.00"
   ↓
   Database: Insert into `invoices` table
   {
     "job_id": 123,
     "subtotal": 1150.00,
     "tax": 0.00,
     "total": 1150.00,
     "status": "pending",
     "line_items": [...]
   }
   ↓
   Generate PDF: Invoice with plain language descriptions
   ↓
   Desktop App: Display invoice preview

┌─────────────────────────────────────────────────────────────┐
│ 5. PAYMENT PROCESSING                                      │
└─────────────────────────────────────────────────────────────┘
   Desktop App → POST /api/paypal/create-payment
   {
     "invoice_id": 456,
     "amount": 1150.00
   }
   ↓
   PayPal API: Create payment
   ↓
   Return: Payment URL
   ↓
   Customer: Clicks link → Pays via PayPal
   ↓
   PayPal Webhook → POST /api/paypal/webhook
   {
     "event": "PAYMENT.COMPLETED",
     "invoice_id": 456
   }
   ↓
   Database: Update `invoices` table
   {
     "status": "paid",
     "paid_at": "2025-01-17T15:30:00"
   }
   ↓
   Database: Insert into `payment_transactions` table
   {
     "invoice_id": 456,
     "amount": 1150.00,
     "method": "paypal",
     "status": "completed"
   }
```

---

## Database Schema

### Core Tables

**`customers`**
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**`jobs`**
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    address TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    -- Pricing progression
    base_estimate DECIMAL(10,2) DEFAULT 0.00,      -- Sum of AI room costs
    ai_estimate DECIMAL(10,2) DEFAULT 0.00,        -- Base + AI adjustments
    human_adjusted_estimate DECIMAL(10,2) DEFAULT 0.00,  -- After human override
    final_price DECIMAL(10,2) DEFAULT 0.00,        -- What customer pays
    -- Metadata
    scheduled_date TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Status values**: `scheduled`, `in_progress`, `completed`, `invoiced`, `paid`, `cancelled`

**`rooms`**
```sql
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id),
    room_name VARCHAR(255) NOT NULL,

    -- AI Classification (preserved for audit)
    ai_size_class VARCHAR(50),           -- small/medium/large/extra_large
    ai_workload_class VARCHAR(50),       -- light/moderate/heavy/extreme
    ai_confidence DECIMAL(5,4),          -- 0.0000 to 1.0000
    ai_reasoning TEXT,                   -- AI's explanation
    ai_features JSONB,                   -- {furniture_count, hazards, etc}

    -- Human Override (authoritative)
    human_size_class VARCHAR(50),
    human_workload_class VARCHAR(50),
    human_override_reason TEXT,

    -- Final Classification (used for pricing)
    final_size_class VARCHAR(50),        -- human OR ai
    final_workload_class VARCHAR(50),    -- human OR ai

    -- Pricing
    estimated_cost DECIMAL(10,2),

    -- Image
    image_url TEXT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**`invoices`**
```sql
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id),
    invoice_number VARCHAR(50) UNIQUE,
    subtotal DECIMAL(10,2) NOT NULL,
    tax DECIMAL(10,2) DEFAULT 0.00,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    due_date DATE,
    paid_at TIMESTAMP,
    line_items JSONB,                    -- Array of invoice items
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Status values**: `pending`, `sent`, `paid`, `overdue`, `cancelled`

**`payment_transactions`**
```sql
CREATE TABLE payment_transactions (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id),
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(50),                  -- paypal, stripe, cash, check
    status VARCHAR(50) DEFAULT 'pending',
    transaction_id VARCHAR(255),         -- External payment ID
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**`pricing_rules`**
```sql
CREATE TABLE pricing_rules (
    id SERIAL PRIMARY KEY,
    rule_type VARCHAR(50) NOT NULL,      -- size_multiplier, workload_multiplier, adjustment
    key VARCHAR(100) NOT NULL,           -- small, medium, stairs, etc.
    value DECIMAL(10,4),                 -- Multiplier (1.5) or flat fee (150)
    active BOOLEAN DEFAULT TRUE,
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**`sync_queue`** (for offline mobile sync)
```sql
CREATE TABLE sync_queue (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    operation VARCHAR(50),               -- create_room, update_job, etc.
    entity_type VARCHAR(50),             -- room, job, customer
    entity_id INTEGER,
    payload JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    retries INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);
```

**`audit_log`**
```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(100),                 -- update_room_classification
    entity_type VARCHAR(50),
    entity_id INTEGER,
    old_value JSONB,
    new_value JSONB,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Relationships

```
customers (1) ──── (many) jobs
jobs (1) ──── (many) rooms
jobs (1) ──── (many) invoices
invoices (1) ──── (many) payment_transactions
```

---

## AI Integration

### Ollama LLaVA Setup

**Installation**:
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull LLaVA model (7B parameter version)
ollama pull llava:7b

# Start Ollama server
ollama serve
```

**Verification**:
```bash
curl http://localhost:11434/api/tags
```

### AI Vision Service Architecture

**File**: `backend/services/ai_vision.py`

```python
class AIVisionService:
    def __init__(self, ollama_url: str):
        self.ollama_url = ollama_url
        self.model = "llava:7b"

    def classify_room(self, image_path: str, room_name: str = ""):
        """
        Analyze room image using LLaVA vision model.

        Returns:
            {
                "size_class": "large",
                "workload_class": "heavy",
                "confidence": 0.87,
                "reasoning": "...",
                "features": {...}
            }
        """
        prompt = self._build_ultrathink_prompt(room_name)
        response = self._call_ollama(image_path, prompt)
        return self._parse_response(response)

    def _build_ultrathink_prompt(self, room_name: str):
        """Extended reasoning prompt for higher accuracy."""
        return f"""
        Analyze this room photo for a junk removal estimate.
        Room: {room_name or 'Unknown'}

        STEP 1 - Dimensions:
        - Estimate room size based on furniture scale
        - Small: <100 sq ft (closet, half bath)
        - Medium: 100-200 sq ft (bedroom, office)
        - Large: 200-400 sq ft (master bedroom, kitchen)
        - Extra Large: >400 sq ft (garage, basement)

        STEP 2 - Clutter Density:
        - Count visible furniture pieces
        - Assess loose item density
        - Identify boxes, bags, clutter piles

        STEP 3 - Workload Complexity:
        - Light: Minimal items, easy to carry
        - Moderate: Normal clutter, some furniture
        - Heavy: High clutter, furniture disassembly needed
        - Extreme: Hoarding, hazmat, access issues

        STEP 4 - Special Factors:
        - Stairs required?
        - Narrow doorways?
        - Heavy furniture (piano, safe, etc.)?
        - Hazards (mold, chemicals, sharp objects)?

        Return JSON:
        {{
          "size_class": "small|medium|large|extra_large",
          "workload_class": "light|moderate|heavy|extreme",
          "confidence": 0.0-1.0,
          "reasoning": "Your analysis...",
          "features": {{
            "furniture_count": int,
            "clutter_density": "low|medium|high",
            "stairs_required": boolean,
            "hazards": [...]
          }}
        }}
        """
```

### AI Accuracy Metrics

**Target Metrics**:
- Confidence score: >0.75 for production use
- Agreement with human: >80% on size classification
- Agreement with human: >75% on workload classification

**Monitoring**:
- Track `ai_confidence` distribution
- Compare `ai_*_class` vs `human_*_class` fields
- Alert if average confidence drops below 0.70

---

## API Structure

### Base URL

```
Production: https://cleanoutpro-production.up.railway.app
Development: http://localhost:8000
```

### Authentication

**Current**: None (open API)
**Future**: JWT Bearer tokens

```
Authorization: Bearer {token}
```

### Core Endpoints

**Health Check**
```
GET /
Response: {"message": "CleanoutPro API is running"}
```

**Jobs**
```
GET    /api/jobs              List all jobs
GET    /api/jobs/{id}         Get job details (includes rooms)
POST   /api/jobs              Create job
PUT    /api/jobs/{id}         Update job
DELETE /api/jobs/{id}         Delete job
```

**Rooms**
```
POST   /api/rooms/classify    Upload photo + classify
GET    /api/jobs/{id}/rooms   List rooms for job
GET    /api/rooms/{id}        Get room details
PUT    /api/rooms/{id}        Update room (human override)
DELETE /api/rooms/{id}        Delete room
```

**Customers**
```
GET    /api/customers         List all customers
GET    /api/customers/{id}    Get customer details
POST   /api/customers         Create customer
PUT    /api/customers/{id}    Update customer
DELETE /api/customers/{id}    Delete customer
```

**Invoices**
```
POST   /api/invoices          Generate invoice
GET    /api/invoices/{id}     Get invoice
PUT    /api/invoices/{id}     Update invoice
```

**PayPal**
```
POST   /api/paypal/create-payment    Create payment
POST   /api/paypal/webhook           Payment webhook
```

**Sync** (future)
```
POST   /api/sync/upload       Upload offline operations
GET    /api/sync/download     Download latest data
```

### Error Responses

All errors follow this format:
```json
{
  "detail": "Error message here"
}
```

**HTTP Status Codes**:
- `200` - Success
- `201` - Created
- `400` - Bad request (validation error)
- `404` - Not found
- `422` - Unprocessable entity
- `500` - Internal server error

---

## Pricing Engine

### Implementation

**File**: `backend/services/pricing_engine.py`

```python
class PricingEngine:
    BASE_LABOR = 150.00

    SIZE_MULTIPLIERS = {
        "small": 1.0,
        "medium": 1.5,
        "large": 2.0,
        "extra_large": 3.0
    }

    WORKLOAD_MULTIPLIERS = {
        "light": 1.0,
        "moderate": 1.3,
        "heavy": 1.6,
        "extreme": 2.0
    }

    def calculate_room_cost(self, size_class: str, workload_class: str):
        """Calculate single room cost."""
        size_mult = self.SIZE_MULTIPLIERS.get(size_class, 1.0)
        workload_mult = self.WORKLOAD_MULTIPLIERS.get(workload_class, 1.0)
        return self.BASE_LABOR * size_mult * workload_mult

    def calculate_job_total(self, rooms: list, adjustments: list):
        """Calculate total job cost."""
        room_total = sum(room.estimated_cost for room in rooms)
        adjustment_total = sum(adj.cost for adj in adjustments)
        return room_total + adjustment_total

    def generate_invoice_line_items(self, job):
        """Generate plain language invoice items (NO AI JARGON)."""
        items = []

        # Room line items
        for room in job.rooms:
            items.append({
                "description": f"{room.room_name} Cleanout",
                "amount": room.estimated_cost
            })

        # Adjustment line items
        for adj in job.adjustments:
            items.append({
                "description": adj.description,  # e.g., "Stair Access (2 flights)"
                "amount": adj.cost
            })

        return items
```

### Invoice Line Item Rules

**✅ GOOD Examples**:
```
Master Bedroom Cleanout - $450.00
Kitchen Cleanout - $292.50
Stair Access (2 flights) - $50.00
Bin Rental (20-yard) - $200.00
```

**❌ BAD Examples** (NEVER do this):
```
Master Bedroom (AI: Large/Heavy, 87% confidence) - $450.00
Kitchen (AI Classification: Medium/Moderate) - $292.50
Stairs (AI detected: 2 flights) - $50.00
```

**Rule**: Customers must NEVER see AI terminology in invoices. They don't care how the estimate was calculated, only what they're paying for.

---

## Current Implementation Status

### ✅ Complete (Production Ready)

**Backend API**:
- [x] FastAPI server running
- [x] PostgreSQL database (Neon.tech)
- [x] All CRUD endpoints (jobs, rooms, customers)
- [x] AI vision service (Ollama LLaVA)
- [x] Pricing engine with multipliers
- [x] Image upload and storage
- [x] CORS configuration
- [x] Error handling
- [x] Health check endpoint
- [x] Deployed to Railway/Render

**Database**:
- [x] Schema created (`schemas.sql`)
- [x] ORM models (SQLAlchemy)
- [x] Relationships configured
- [x] Triggers for `updated_at`
- [x] Audit log structure

**Documentation**:
- [x] `CLAUDE.md` - Project overview
- [x] `API_QUICKSTART.md` - API guide
- [x] `DEPLOYMENT_STATUS.md` - Deployment info
- [x] `IPHONE_SETUP.md` - Mobile setup guide
- [x] `DEVELOPER_API_GUIDE.md` - Developer docs
- [x] `SYSTEM_OVERVIEW.md` - This document

### 🚧 In Progress

**Mobile Web (PWA)**:
- [x] Basic HTML/CSS/JS interface
- [x] Camera integration
- [x] API connection
- [x] Add to home screen support
- [ ] Deploy to production
- [ ] User testing

### 📋 Not Started (TODO)

**Mobile App (React Native)**:
- [ ] Project initialization
- [ ] Camera integration
- [ ] API service layer
- [ ] Offline storage
- [ ] Sync queue
- [ ] GPS location
- [ ] Push notifications
- [ ] iOS build
- [ ] Android build
- [ ] TestFlight beta
- [ ] App Store submission

**Desktop App (Electron)**:
- [ ] Project initialization
- [ ] 3D visualization (Three.js)
- [ ] Table view fallback
- [ ] Job management UI
- [ ] Estimate review interface
- [ ] Invoice generator
- [ ] PayPal integration
- [ ] PDF export
- [ ] Windows build
- [ ] macOS build

**Backend Enhancements**:
- [ ] JWT authentication
- [ ] User management
- [ ] Role-based access control
- [ ] WebSocket real-time sync
- [ ] Redis caching
- [ ] Image compression
- [ ] Cloudinary integration
- [ ] Webhook system
- [ ] Analytics/reporting endpoints

---

## Deployment Architecture

### Production Stack (Free Tier)

```
┌─────────────────────────────────────────────────────────────┐
│                     USER DEVICES                            │
│  - iPhone/Android (Mobile App)                              │
│  - Windows/Mac (Desktop App)                                │
│  - Web Browser (PWA)                                        │
└──────────────┬──────────────────────────────────────────────┘
               │
               │ HTTPS
               ▼
┌─────────────────────────────────────────────────────────────┐
│               CLOUDFLARE (DNS + SSL)                        │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│          RAILWAY / RENDER (Backend Hosting)                 │
│  - Docker container                                          │
│  - Auto-deploy from GitHub                                  │
│  - Free tier: 500 hours/month                               │
└──────────────┬──────────────────────────────────────────────┘
               │
               ├─────────────────┬─────────────────┐
               ▼                 ▼                 ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  NEON.TECH       │  │  UPSTASH         │  │  CLOUDINARY      │
│  (PostgreSQL)    │  │  (Redis)         │  │  (Image CDN)     │
│  Free: 512MB     │  │  Free: 10K req   │  │  Free: 25 GB     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

### Cost Breakdown (MVP)

| Service | Plan | Cost | Notes |
|---------|------|------|-------|
| **Railway/Render** | Free Tier | $0 | 500 hours/month |
| **Neon.tech** | Free | $0 | 512MB database |
| **Upstash** | Free | $0 | 10K requests/day |
| **Cloudinary** | Free | $0 | 25GB storage |
| **Domain** | Cloudflare | $10/year | Optional |
| **Total** | | $10/year | Nearly free! |

**Scaling costs** (if needed):
- Railway Pro: $20/month (unlimited hours)
- Neon Pro: $19/month (1GB database)
- Upstash Pro: $10/month (100K requests/day)
- **Total at scale**: ~$50/month

### Deployment Process

**Backend (Railway)**:
```bash
# 1. Push to GitHub
git push origin main

# 2. Railway auto-deploys
# - Builds Docker container
# - Runs database migrations
# - Starts FastAPI server
# - Provides public URL
```

**Mobile Web (Netlify)**:
```bash
# Drag and drop mobile-web/ folder to netlify.com
# Or connect to GitHub for auto-deploy
```

**Mobile App (TestFlight)**:
```bash
# Build in Xcode
# Archive → Distribute to App Store Connect
# Add testers → Send TestFlight invites
```

**Desktop App**:
```bash
# Build with Electron Forge
npm run make
# Distributes .exe (Windows) or .dmg (Mac)
```

---

## Security Considerations

### Current Security Posture

**✅ Implemented**:
- HTTPS required (Railway/Render enforce SSL)
- CORS configured for mobile/desktop apps
- SQL injection protection (SQLAlchemy ORM)
- Input validation (Pydantic models)

**⚠️ Missing (TODO)**:
- [ ] Authentication (JWT tokens)
- [ ] Authorization (role-based access)
- [ ] Rate limiting (prevent abuse)
- [ ] API key for mobile apps
- [ ] File upload size limits
- [ ] Image content validation (prevent malicious uploads)
- [ ] Audit logging (track all changes)
- [ ] Secrets management (environment variables)

### Recommended Security Enhancements

**Phase 1 (Critical)**:
1. Add JWT authentication
2. Implement rate limiting
3. Add file upload validation
4. Enable audit logging

**Phase 2 (Important)**:
5. Add API key authentication for mobile
6. Implement role-based access (admin, field, office)
7. Add input sanitization
8. Enable database encryption at rest

**Phase 3 (Nice-to-have)**:
9. Two-factor authentication
10. IP whitelisting for admin
11. Penetration testing
12. SOC 2 compliance (if handling credit cards)

---

## Future Roadmap

### Q1 2025 - MVP Launch

**Goal**: Get first paying customer

- [ ] Complete mobile web (PWA) deployment
- [ ] User testing with field workers
- [ ] Bug fixes and UX improvements
- [ ] Basic authentication (JWT)
- [ ] Invoice generation
- [ ] PayPal integration
- [ ] 10 beta customers

### Q2 2025 - Native Apps

**Goal**: Launch iOS and Android apps

- [ ] React Native mobile app (iOS + Android)
- [ ] TestFlight beta testing
- [ ] App Store submission
- [ ] Google Play submission
- [ ] Push notifications
- [ ] Offline mode
- [ ] 50 paying customers

### Q3 2025 - Desktop App

**Goal**: Office staff can review and invoice

- [ ] Electron desktop app
- [ ] 3D visualization
- [ ] Estimate review interface
- [ ] Invoice generator (PDF)
- [ ] PayPal integration
- [ ] Windows and Mac builds
- [ ] 100 paying customers

### Q4 2025 - Advanced Features

**Goal**: Scale to 500 customers

- [ ] Multi-user support (teams)
- [ ] Role-based access control
- [ ] Advanced reporting (analytics)
- [ ] Customer portal (view invoices)
- [ ] SMS notifications
- [ ] Automated follow-ups
- [ ] AI model fine-tuning (improve accuracy)
- [ ] Integration marketplace (QuickBooks, etc.)

### 2026+ - Enterprise

**Goal**: 10,000+ customers

- [ ] White-label solution
- [ ] Multi-tenancy
- [ ] Custom pricing rules per customer
- [ ] Advanced AI (multi-room analysis)
- [ ] Video analysis (instead of photos)
- [ ] AR visualization (customer preview)
- [ ] Franchise management features
- [ ] Enterprise SLA

---

## Appendix: Key Files

### Backend Structure

```
backend/
├── api/
│   ├── main.py                 # FastAPI app, CORS, routes
│   └── routes/
│       ├── jobs.py             # Job endpoints
│       ├── rooms.py            # Room endpoints + classify
│       ├── customers.py        # Customer endpoints
│       ├── invoices.py         # Invoice endpoints
│       └── paypal.py           # PayPal integration
├── database/
│   ├── connection.py           # SQLAlchemy engine
│   ├── models.py               # ORM models
│   └── schemas.sql             # PostgreSQL schema
├── services/
│   ├── ai_vision.py            # Ollama LLaVA integration
│   ├── pricing_engine.py       # Cost calculation
│   └── sync_service.py         # Offline sync (future)
├── utils/
│   ├── auth.py                 # JWT helpers (future)
│   └── validators.py           # Input validation
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # Backend docs
```

### Mobile Web Structure

```
mobile-web/
├── index.html                  # Main PWA interface
├── manifest.json               # PWA configuration
├── sw.js                       # Service worker (offline)
└── README.md                   # Deployment guide
```

### Documentation

```
/
├── CLAUDE.md                   # Project overview (for AI)
├── API_QUICKSTART.md           # API usage guide
├── DEPLOYMENT_STATUS.md        # Current deployment info
├── IPHONE_SETUP.md             # iPhone/mobile guide
├── DEVELOPER_API_GUIDE.md      # Developer documentation
└── SYSTEM_OVERVIEW.md          # This document
```

---

## Summary

CleanoutPro is a **three-tier AI-powered business management system** designed to:

1. **Capture** - Field workers photograph rooms on mobile devices
2. **Classify** - AI analyzes photos and estimates size/workload
3. **Calculate** - Pricing engine applies multipliers for accurate quotes
4. **Review** - Office staff override AI when needed
5. **Invoice** - Generate professional invoices with plain language
6. **Collect** - Process payments via PayPal integration

**Current Status**: Backend is production-ready, mobile apps in development

**Tech Stack**: FastAPI + PostgreSQL + Ollama LLaVA + React Native (future)

**Deployment**: Railway (backend) + Neon (database) + Netlify (mobile web)

**Cost**: $0-10/year for MVP, $50/month at scale

**Timeline**: MVP ready now, full native apps Q2 2025

---

**For more information**:
- Development questions: See `CLAUDE.md`
- API integration: See `DEVELOPER_API_GUIDE.md`
- iPhone setup: See `IPHONE_SETUP.md`
- Deployment: See `DEPLOYMENT_STATUS.md`

**End of System Overview**
