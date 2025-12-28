"""
Michigan Autonomous Client Acquisition API Routes
Integrates autonomous lead generation and deal closing with existing backend
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import logging
from datetime import datetime

# Local imports
from database.connection import get_db
from api.routes.jobs import Job
from api.routes.rooms import Room
from services.pricing_engine import PricingEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/michigan", tags=["michigan"])


# Pydantic models
class MichiganLeadResponse(BaseModel):
    id: int
    source: str
    title: str
    description: Optional[str]
    location: str
    urgency_score: float
    estimated_value: float
    lead_type: str
    contacted: bool
    quoted: bool


class MichiganQuoteRequest(BaseModel):
    lead_id: int
    customer_name: str
    property_address: str
    contact_email: Optional[str]
    contact_phone: Optional[str]


class MichiganQuoteResponse(BaseModel):
    quote_id: str
    customer_name: str
    property_address: str
    estimated_cost: float
    discount_amount: float
    final_price: float
    estimated_duration: str
    available_slots: List[str]
    expires_at: str


class MichiganCampaignRequest(BaseModel):
    campaign_type: str  # 'lead_generation', 'outreach', 'quoting'
    location_filter: Optional[str] = None
    urgency_threshold: Optional[float] = 0.4


class MichiganCampaignResponse(BaseModel):
    campaign_id: str
    status: str
    leads_processed: int
    emails_sent: int
    quotes_generated: int
    estimated_revenue: float


class MichiganAnalyticsResponse(BaseModel):
    total_leads: int
    leads_contacted: int
    quotes_sent: int
    conversion_rate: float
    average_job_value: float
    top_locations: List[Dict[str, str]]
    recent_performance: List[Dict[str, str]]


# Import Michigan services (simplified for demo)
try:
    from services.michigan_autonomous import MichiganAutonomousSystem

    MICHIGAN_SYSTEM_AVAILABLE = True
except ImportError:
    logger.warning("Michigan autonomous system not available - using demo data")
    MICHIGAN_SYSTEM_AVAILABLE = False

# Global orchestrator instance
michigan_orchestrator = None


def get_michigan_system():
    """Get or create Michigan autonomous system instance"""
    global michigan_orchestrator
    if not michigan_orchestrator and MICHIGAN_SYSTEM_AVAILABLE:
        from services.michigan_autonomous import MichiganAutonomousSystem

        michigan_orchestrator = MichiganAutonomousSystem()
    return michigan_orchestrator


@router.get("/leads", response_model=List[MichiganLeadResponse])
async def get_michigan_leads(
    skip: int = 0,
    limit: int = 50,
    location: Optional[str] = None,
    urgency_min: Optional[float] = None,
    contacted: Optional[bool] = None,
):
    """Get Michigan leads with filtering options"""
    try:
        system = get_michigan_system()
        if not system:
            # Return demo data
            return [
                MichiganLeadResponse(
                    id=1,
                    source="facebook_marketplace",
                    title="Urgent house cleanout needed",
                    description="Need to clear entire house before moving",
                    location="Detroit",
                    urgency_score=0.9,
                    estimated_value=450.0,
                    lead_type="urgent_cleanout",
                    contacted=False,
                    quoted=False,
                ),
                MichiganLeadResponse(
                    id=2,
                    source="craigslist",
                    title="Basement junk removal",
                    description="Old furniture and debris in basement",
                    location="Royal Oak",
                    urgency_score=0.4,
                    estimated_value=250.0,
                    lead_type="cleanout",
                    contacted=True,
                    quoted=False,
                ),
            ]

        # Query real leads from database
        query = "SELECT * FROM leads WHERE 1=1"
        params = []

        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")

        if urgency_min:
            query += " AND urgency_score >= ?"
            params.append(urgency_min)

        if contacted is not None:
            query += " AND contacted = ?"
            params.append(contacted)

        query += " ORDER BY urgency_score DESC, created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, skip])

        cursor = system.db_conn.cursor()
        cursor.execute(query, params)

        leads = []
        for row in cursor.fetchall():
            lead = dict(zip([col[0] for col in cursor.description], row))
            leads.append(MichiganLeadResponse(**lead))

        return leads

    except Exception as e:
        logger.error(f"Error getting Michigan leads: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve leads")


@router.post("/quotes/generate", response_model=MichiganQuoteResponse)
async def generate_michigan_quote(
    request: MichiganQuoteRequest, background_tasks: BackgroundTasks
):
    """Generate Michigan-specific quote for a lead"""
    try:
        system = get_michigan_system()
        if not system:
            # Return demo quote
            return MichiganQuoteResponse(
                quote_id="MI-DEMO-1234",
                customer_name=request.customer_name,
                property_address=request.property_address,
                estimated_cost=300.0,
                discount_amount=30.0,
                final_price=270.0,
                estimated_duration="2-4 hours",
                available_slots=[
                    "2024-01-15 09:00 AM",
                    "2024-01-15 02:00 PM",
                    "2024-01-16 09:00 AM",
                ],
                expires_at="2024-01-17 12:00 PM",
            )

        # Generate real quote
        from services.michigan_deal_closer import MichiganDealCloser

        deal_closer = MichiganDealCloser(system.db_conn)

        # Get lead data
        cursor = system.db_conn.cursor()
        cursor.execute("SELECT * FROM leads WHERE id = ?", (request.lead_id,))
        lead_data = cursor.fetchone()

        if not lead_data:
            raise HTTPException(status_code=404, detail="Lead not found")

        lead_dict = dict(zip([col[0] for col in cursor.description], lead_data))

        # Calculate quote
        quote = deal_closer.calculate_michigan_pricing(lead_dict)
        quote_doc = deal_closer.generate_quote_document(quote)

        # Save quote to database
        deal_closer.save_quote_to_database(lead_dict, quote, quote_doc)

        # Send quote in background
        if request.contact_email:
            background_tasks.add_task(
                deal_closer.send_quote_via_email, lead_dict, quote, quote_doc
            )

        return MichiganQuoteResponse(
            quote_id=quote.quote_id,
            customer_name=quote.customer_name,
            property_address=quote.property_address,
            estimated_cost=float(quote.estimated_cost),
            discount_amount=float(quote.michigan_discount),
            final_price=float(quote.final_price),
            estimated_duration=quote.estimated_duration,
            available_slots=[
                slot.strftime("%Y-%m-%d %I:%M %p") for slot in quote.available_slots[:5]
            ],
            expires_at=quote.quote_expires.strftime("%Y-%m-%d %I:%M %p"),
        )

    except Exception as e:
        logger.error(f"Error generating Michigan quote: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate quote")


@router.post("/campaigns/run", response_model=MichiganCampaignResponse)
async def run_michigan_campaign(
    request: MichiganCampaignRequest, background_tasks: BackgroundTasks
):
    """Run Michigan autonomous campaign"""
    try:
        campaign_id = f"MI-CAM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        system = get_michigan_system()
        if not system:
            # Return demo response
            return MichiganCampaignResponse(
                campaign_id=campaign_id,
                status="completed",
                leads_processed=25,
                emails_sent=18,
                quotes_generated=8,
                estimated_revenue=2400.0,
            )

        # Run campaign in background
        if request.campaign_type == "lead_generation":
            background_tasks.add_task(system.run_lead_generation)
        elif request.campaign_type == "outreach":
            background_tasks.add_task(system.run_outreach_campaign)
        elif request.campaign_type == "quoting":
            background_tasks.add_task(system.run_deal_closing)
        else:
            background_tasks.add_task(system.run_autonomous_cycle)

        return MichiganCampaignResponse(
            campaign_id=campaign_id,
            status="started",
            leads_processed=0,
            emails_sent=0,
            quotes_generated=0,
            estimated_revenue=0.0,
        )

    except Exception as e:
        logger.error(f"Error running Michigan campaign: {e}")
        raise HTTPException(status_code=500, detail="Failed to run campaign")


@router.get("/analytics", response_model=MichiganAnalyticsResponse)
async def get_michigan_analytics():
    """Get Michigan autonomous system analytics"""
    try:
        system = get_michigan_system()
        if not system:
            # Return demo analytics
            return MichiganAnalyticsResponse(
                total_leads=156,
                leads_contacted=89,
                quotes_sent=34,
                conversion_rate=0.28,
                average_job_value=325.50,
                top_locations=[
                    {"location": "Detroit", "leads": 45},
                    {"location": "Royal Oak", "leads": 28},
                    {"location": "Ann Arbor", "leads": 22},
                ],
                recent_performance=[
                    {"date": "2024-01-14", "leads": 12, "quotes": 5},
                    {"date": "2024-01-13", "leads": 8, "quotes": 3},
                    {"date": "2024-01-12", "leads": 15, "quotes": 7},
                ],
            )

        # Get real analytics
        cursor = system.db_conn.cursor()

        # Lead stats
        cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM leads WHERE contacted = TRUE")
        leads_contacted = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM quotes")
        quotes_sent = cursor.fetchone()[0]

        # Conversion rates
        conversion_rate = quotes_sent / max(leads_contacted, 1)

        # Average job value
        cursor.execute("SELECT AVG(final_price) FROM quotes WHERE status = 'accepted'")
        avg_value = cursor.fetchone()[0] or 0

        # Top locations
        cursor.execute("""
            SELECT location, COUNT(*) as count 
            FROM leads 
            GROUP BY location 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_locations = [
            {"location": row[0], "leads": row[1]} for row in cursor.fetchall()
        ]

        # Recent performance
        cursor.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as leads
            FROM leads 
            WHERE created_at >= DATE('now', '-7 days')
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        """)
        recent_performance = [
            {"date": row[0], "leads": row[1], "quotes": 0} for row in cursor.fetchall()
        ]

        return MichiganAnalyticsResponse(
            total_leads=total_leads,
            leads_contacted=leads_contacted,
            quotes_sent=quotes_sent,
            conversion_rate=conversion_rate,
            average_job_value=avg_value,
            top_locations=top_locations,
            recent_performance=recent_performance,
        )

    except Exception as e:
        logger.error(f"Error getting Michigan analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")


@router.get("/status")
async def get_michigan_status():
    """Get Michigan autonomous system status"""
    try:
        system = get_michigan_system()
        if not system:
            return {
                "status": "demo_mode",
                "running": False,
                "last_update": datetime.now().isoformat(),
                "services_available": ["demo_only"],
            }

        status = system.get_system_status()
        return status

    except Exception as e:
        logger.error(f"Error getting Michigan status: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve status")


@router.post("/start")
async def start_michigan_system(background_tasks: BackgroundTasks):
    """Start Michigan autonomous system"""
    try:
        system = get_michigan_system()
        if not system:
            raise HTTPException(status_code=503, detail="Michigan system not available")

        # Start in background
        background_tasks.add_task(system.start_autonomous_mode)

        return {
            "message": "Michigan autonomous system started",
            "status": "starting",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error starting Michigan system: {e}")
        raise HTTPException(status_code=500, detail="Failed to start system")


@router.post("/stop")
async def stop_michigan_system():
    """Stop Michigan autonomous system"""
    try:
        system = get_michigan_system()
        if not system:
            raise HTTPException(status_code=503, detail="Michigan system not available")

        system.stop_autonomous_mode()

        return {
            "message": "Michigan autonomous system stopped",
            "status": "stopped",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error stopping Michigan system: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop system")
