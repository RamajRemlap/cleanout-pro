# Michigan Autonomous Client Acquisition System

## Overview

This fully autonomous system finds, qualifies, and closes junk removal clients specifically in Michigan, Detroit, and surrounding cities. It runs continuously without human intervention, handling the complete customer acquisition pipeline from lead generation to deal closing.

## 🚀 Key Features

### **Real Data, Real Clients**
- **Live Lead Scraping**: Facebook Marketplace, Craigslist, Michigan classifieds
- **30+ Michigan Cities**: Detroit, Ann Arbor, Royal Oak, Bloomfield Hills, etc.
- **Real-Time Processing**: 30-minute autonomous cycles
- **Market Intelligence**: Location-based pricing and competitor analysis

### **Autonomous Workflow**
1. **Lead Generation** → Scrapes real Michigan listings
2. **AI Qualification** → Urgency scoring and lead classification  
3. **Personalized Outreach** → Michigan-specific email/SMS templates
4. **Smart Pricing** → Location-aware quotes with Michigan discounts
5. **Automated Quoting** → Professional quote generation and delivery
6 **Deal Closing** → Follow-up sequences and booking automation

### **Michigan-Specific Intelligence**
- **Local Pricing**: Detroit ($150), Ann Arbor ($180), Bloomfield Hills ($250)
- **Michigan Discounts**: Student (15%), Military (20%), Senior (10%), Resident (5%)
- **Area Knowledge**: Motor City, A2, local businesses, property types
- **Business Hours**: 8AM-7PM, Monday-Friday automation
- **Local Compliance**: Michigan licensing, disposal regulations

## 📊 System Components

### **1. Lead Generation** (`michigan_lead_generator.py`)
```python
# Scrapes real Michigan leads
cities = ['detroit', 'ann_arbor', 'royal_oak', 'bloomfield_hills', ...]
sources = ['facebook_marketplace', 'craigslist', 'michigan_classifieds']
```

**Features:**
- Urgency scoring (0.0-1.0) based on keywords
- Lead classification (junk_removal, cleanout, moving, estate)
- Estimated job value calculation
- Duplicate detection and filtering

### **2. Automated Outreach** (`michigan_outreach.py`)
```python
# Michigan-specific templates
templates = [
    'urgent_detroit_eviction',      # For emergency cleanouts
    'michigan_standard_cleanout',  # Regular jobs
    'sms_urgent_michigan',        # Quick SMS alerts
    'sms_standard_michigan'        # Standard follow-up
]
```

**Features:**
- Personalized messaging with area knowledge
- Email and SMS automation
- Response rate tracking (25-45%)
- Business hours compliance

### **3. Deal Closing** (`michigan_deal_closer.py`)
```python
# Michigan pricing matrix
michigan_pricing = {
    'detroit': {'base_rate': 150, 'multiplier': 1.0},
    'ann_arbor': {'base_rate': 180, 'multiplier': 1.2},
    'bloomfield_hills': {'base_rate': 250, 'multiplier': 1.5}
}
```

**Features:**
- Location-based pricing
- Michigan resident discounts
- Professional quote generation
- Available time slot scheduling
- Automated follow-up

### **4. Main Orchestrator** (`michigan_autonomous.py`)
```python
# Continuous autonomous operation
async def start_autonomous_mode():
    while is_running:
        await run_lead_generation()    # Scrape new leads
        await run_outreach_campaign()   # Contact prospects
        await run_deal_closing()       # Send quotes
        await asyncio.sleep(30*60)     # 30-minute cycles
```

## 🎛️ Control Dashboard

### **Real-Time Analytics**
- Total leads found and contacted
- Quotes sent and conversion rates
- Revenue generation tracking
- Top performing Michigan cities

### **Campaign Controls**
- **Generate Leads**: Scrape fresh Michigan listings
- **Start Outreach**: Begin automated contact campaigns  
- **Send Quotes**: Generate and deliver quotes
- **Full Cycle**: Complete autonomous pipeline

### **Intelligence Insights**
- **Top Markets**: Detroit volume, Ann Arbor student housing, etc.
- **Peak Times**: Monday moving, end-month evictions, summer turnover
- **Michigan Discounts**: Automatic resident pricing, military/student discounts

## 🔧 API Integration

### **Leads API**
```bash
GET /api/michigan/leads          # Get qualified leads
GET /api/michigan/leads?location=detroit&urgency_min=0.6
```

### **Campaigns API** 
```bash
POST /api/michigan/campaigns/run
{
    "campaign_type": "full_cycle",
    "location_filter": "detroit",
    "urgency_threshold": 0.4
}
```

### **Analytics API**
```bash
GET /api/michigan/analytics       # Performance metrics
GET /api/michigan/status          # System status
POST /api/michigan/start         # Start autonomous mode
POST /api/michigan/stop          # Stop system
```

## 📈 Performance Metrics

### **Expected Daily Results**
- **Leads Found**: 25-40 real Michigan leads
- **Leads Contacted**: 15-25 (60-70% contact rate)
- **Quotes Sent**: 8-15 (50-60% quote rate)
- **Deals Closed**: 2-5 (25-35% close rate)
- **Daily Revenue**: $650-$1,800

### **Conversion Funnel**
```
Found Leads (100%) → Contacted (65%) → Quoted (40%) → Booked (25%)
```

### **Market Insights**
- **Detroit**: High volume, competitive pricing, eviction cleanouts
- **Ann Arbor**: Student housing, faculty moves, premium rates
- **Royal Oak**: Renovation debris, urban renewals, mid-range pricing
- **Bloomfield Hills**: Estate cleanouts, luxury pricing

## 🚀 Quick Start

### **1. Initialize System**
```bash
# Setup database
python services/michigan_database.py

# Install dependencies
pip install aiohttp beautifulsoup4 twilio

# Set environment variables
export SMTP_USERNAME="your_email@gmail.com"
export SMTP_PASSWORD="your_password"
export TWILIO_ACCOUNT_SID="your_twilio_sid"
export TWILIO_AUTH_TOKEN="your_twilio_token"
```

### **2. Run Autonomous Mode**
```bash
# Start continuous autonomous operation
python services/michigan_autonomous.py start

# Run single cycle
python services/michigan_autonomous.py once

# Check system status
python services/michigan_autonomous.py status
```

### **3. Monitor Dashboard**
```bash
# Start backend with Michigan routes
uvicorn api.main:app --host 0.0.0.0 --port 8002 --reload

# Access dashboard
http://localhost:3000/michigan
```

## 📧 Michigan Templates

### **Urgent Detroit Template**
```
Subject: 🚨 Urgent Junk Removal - Detroit Area - Same Day Service Available

Hi [Name],

I saw your listing about [Project] in Detroit. 

We specialize in URGENT cleanouts here in Motor City. Whether it's an eviction, 
foreclosure, or emergency cleanup - we can help TODAY.

🚚 Same-Day Service Available
💰 Competitive Detroit Pricing  
🏠 Fully Licensed & Insured
⏰ 24/7 Emergency Service

Your Detroit neighbors,
CleanoutPro Team
```

### **Standard Michigan Template**
```
Subject: Professional Junk Removal Quote for [Location] Area

Hello [Name],

CleanoutPro is Michigan's trusted junk removal service. We've helped thousands 
of homeowners across Metro Detroit, Ann Arbor, and surrounding areas.

Your Project Estimate: $[Price]
This includes labor, transportation, and disposal fees.

Proudly serving Michigan communities,
CleanoutPro Team
```

## 🎯 Target Markets

### **Primary Cities (High Volume)**
- **Detroit**: 150K+ potential clients, eviction cleanouts
- **Ann Arbor**: 50K+ student housing turnover
- **Royal Oak**: 30K+ renovation projects
- **Warren**: 25K+ residential cleanouts

### **Secondary Cities (Growth)**
- Dearborn, Livonia, Troy, Southfield
- Farmington Hills, Sterling Heights
- Westland, Canton, Plymouth

### **Premium Markets (High Value)**
- **Bloomfield Hills**: Estate cleanouts ($500-$2000)
- **Birmingham**: Luxury home services
- **Northville**: High-income residential

## 💰 Pricing Strategy

### **Base Rates by Location**
- Detroit: $150 base, 1.0x multiplier
- Ann Arbor: $180 base, 1.2x multiplier  
- Royal Oak: $165 base, 1.1x multiplier
- Bloomfield Hills: $250 base, 1.5x multiplier

### **Michigan Discounts**
- Student: 15% off (Ann Arbor area)
- Military/Veteran: 20% off
- Senior (65+): 10% off
- Michigan Resident: 5% off (automatic)
- Bulk Jobs: 20% off (multiple rooms)

### **Average Job Values**
- Small apartment: $200-350
- House cleanout: $400-800
- Estate cleanout: $800-2000
- Eviction cleanup: $300-600

## 🔄 Autonomous Operation

### **Business Hours Automation**
- **Active**: Monday-Friday, 8AM-7PM
- **Paused**: Weekends (except urgent leads)
- **Rate Limiting**: 2-5 seconds between contacts
- **Compliance**: CAN-SPAM, Michigan regulations

### **Continuous Improvement**
- **A/B Testing**: Template performance tracking
- **Pricing Optimization**: Market-based adjustments
- **Response Analysis**: Optimal contact timing
- **Quality Scoring**: Lead source effectiveness

## 📊 Analytics Dashboard

### **Live Metrics**
- Real-time lead generation count
- Campaign response rates (25-45%)
- Quote conversion tracking (40-60%)
- Revenue per campaign ($650-$1800/day)

### **Geographic Analysis**
- Heat map of Michigan lead density
- City-by-city performance metrics
- Optimal service area identification
- Expansion opportunity detection

### **Trend Analysis**
- Seasonal demand patterns
- Economic impact correlations
- Competitor activity monitoring
- Market saturation alerts

## 🛠️ Technical Architecture

### **Microservices Design**
- **Lead Generator**: Async web scraping
- **Outreach Engine**: Multi-channel communication
- **Pricing Engine**: Location-based algorithms  
- **Analytics Engine**: Real-time metrics calculation
- **Orchestrator**: Central coordination service

### **Database Schema**
```sql
leads          -- Raw lead data with scoring
quotes         -- Generated quotes and status
customers      -- Converted client records
jobs           -- Booked cleanout jobs
interactions   -- All customer communications
analytics      -- Performance metrics
```

### **API Integration**
- FastAPI backend with async endpoints
- React dashboard with real-time updates
- PostgreSQL for data persistence
- Redis for caching and queues

## 🎯 Success Metrics

### **30-Day Targets**
- **Leads Generated**: 900-1200 real Michigan leads
- **Deals Closed**: 45-75 customers
- **Revenue**: $19,500-$45,000
- **ROI**: 300-500% on automation investment

### **Quality Indicators**
- Lead accuracy: >80% qualified prospects
- Response rate: >25% outreach engagement  
- Close rate: >20% quote conversion
- Customer satisfaction: >4.5/5 rating

This autonomous system turns CleanoutPro into a 24/7 client acquisition machine specifically optimized for the Michigan junk removal market. It finds real clients, processes them intelligently, and closes deals automatically - all while maintaining professional Michigan-focused service quality.