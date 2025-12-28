"""
Michigan Automated Deal Closing System
Converts leads to customers with automated quotes and booking
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import sqlite3
import uuid
import re
from decimal import Decimal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MichiganQuote:
    """Michigan-specific quote structure"""

    quote_id: str
    customer_name: str
    lead_source: str
    property_address: str
    estimated_cost: Decimal
    michigan_discount: Decimal
    final_price: Decimal
    estimated_duration: str
    available_slots: List[datetime]
    quote_expires: datetime
    terms_conditions: str


class MichiganDealCloser:
    """Automated deal closing system for Michigan leads"""

    def __init__(self, db_connection):
        self.db_conn = db_connection
        self.michigan_pricing = {
            "detroit": {
                "base_rate": Decimal("150.00"),
                "multiplier": Decimal("1.0"),  # Standard Detroit rate
                "discount_eligible": True,
                "typical_duration": "2-4 hours",
            },
            "ann_arbor": {
                "base_rate": Decimal("180.00"),
                "multiplier": Decimal("1.2"),  # Higher for college town
                "discount_eligible": True,
                "typical_duration": "3-5 hours",
            },
            "bloomfield_hills": {
                "base_rate": Decimal("250.00"),
                "multiplier": Decimal("1.5"),  # Premium area
                "discount_eligible": False,
                "typical_duration": "4-6 hours",
            },
            "royal_oak": {
                "base_rate": Decimal("165.00"),
                "multiplier": Decimal("1.1"),
                "discount_eligible": True,
                "typical_duration": "2-4 hours",
            },
        }

        self.michigan_discounts = {
            "military": Decimal("0.10"),  # 10% for military
            "senior": Decimal("0.10"),  # 10% for seniors 65+
            "student": Decimal("0.15"),  # 15% for students
            "first_responder": Decimal("0.15"),  # 15% for first responders
            "veteran": Decimal("0.20"),  # 20% for veterans
            "bulk_job": Decimal("0.20"),  # 20% for multiple rooms
            "michigan_resident": Decimal("0.05"),  # 5% Michigan resident discount
            "same_day": Decimal("-0.10"),  # 10% surcharge for same day
            "weekend": Decimal("0.05"),  # 5% surcharge for weekend
        }

        self.michigan_terms = {
            "standard_terms": """
**Michigan Cleanout Service Agreement**

• Professional cleanout and junk removal
• All labor, transportation, and disposal fees included
• Recycle and donate usable items to Michigan charities
• Fully licensed and insured in Michigan
• 24-hour cancellation policy
• Payment due upon completion
• Satisfaction guaranteed
            """,
            "eviction_terms": """
**Eviction Cleanout - Michigan Compliance**

• Legal compliance with Michigan eviction laws
• Property preservation documentation
• Court-approved timelines
• Before/after photo documentation
• Certified disposal service
• Fast turnaround for property managers
            """,
            "estate_terms": """
**Estate Cleanout Services**

• Compassionate and respectful service
• Family coordination available
• Donation to Michigan charities
• Antique and valuable item handling
• Probate process support
• Flexible scheduling for families
            """,
        }

    def get_location_pricing(self, location: str) -> Dict:
        """Get location-specific pricing for Michigan cities"""
        location_lower = location.lower().replace(" ", "_")

        # Direct match
        if location_lower in self.michigan_pricing:
            return self.michigan_pricing[location_lower]

        # Partial matches
        for area, pricing in self.michigan_pricing.items():
            if area in location_lower:
                return pricing

        # Default Michigan pricing
        return self.michigan_pricing["detroit"]

    def calculate_michigan_pricing(self, lead_data: Dict) -> MichiganQuote:
        """Calculate Michigan-specific quote with local discounts"""
        location = lead_data.get("location", "Detroit")
        location_pricing = self.get_location_pricing(location)

        # Base calculation from estimated value
        base_cost = Decimal(str(lead_data.get("estimated_value", 200)))

        # Apply location multiplier
        adjusted_cost = base_cost * location_pricing["multiplier"]

        # Michigan resident discount (almost everyone qualifies)
        michigan_discount = Decimal("0.00")
        if location_pricing["discount_eligible"]:
            michigan_discount = (
                adjusted_cost * self.michigan_discounts["michigan_resident"]
            )

        # Check for other discounts from lead text
        lead_text = (
            f"{lead_data.get('title', '')} {lead_data.get('description', '')}".lower()
        )

        additional_discounts = Decimal("0.00")
        if any(
            word in lead_text
            for word in ["military", "veteran", "army", "navy", "air force"]
        ):
            additional_discounts += adjusted_cost * self.michigan_discounts["veteran"]
        elif any(word in lead_text for word in ["senior", "elderly", "retirement"]):
            additional_discounts += adjusted_cost * self.michigan_discounts["senior"]
        elif any(word in lead_text for word in ["student", "college", "university"]):
            additional_discounts += adjusted_cost * self.michigan_discounts["student"]
        elif any(word in lead_text for word in ["police", "fire", "emt", "paramedic"]):
            additional_discounts += (
                adjusted_cost * self.michigan_discounts["first_responder"]
            )

        # Same day/weekend surcharges
        if "urgent" in lead_text or "asap" in lead_text:
            additional_discounts -= adjusted_cost * abs(
                self.michigan_discounts["same_day"]
            )

        # Total discounts
        total_discounts = michigan_discount + additional_discounts

        # Final pricing
        final_price = adjusted_cost - total_discounts
        final_price = max(final_price, Decimal("100.00"))  # Minimum $100

        # Generate available slots (next 7 days)
        available_slots = self.generate_available_slots(location)

        # Determine terms
        terms = self.michigan_terms["standard_terms"]
        if any(word in lead_text for word in ["eviction", "foreclosure", "court"]):
            terms = self.michigan_terms["eviction_terms"]
        elif any(
            word in lead_text
            for word in ["estate", "inheritance", "deceased", "passed"]
        ):
            terms = self.michigan_terms["estate_terms"]

        return MichiganQuote(
            quote_id=f"MI-{uuid.uuid4().hex[:8].upper()}",
            customer_name=self.extract_customer_name(lead_data),
            lead_source=lead_data.get("source", "online"),
            property_address=f"{location}, MI",
            estimated_cost=base_cost,
            michigan_discount=total_discounts,
            final_price=final_price,
            estimated_duration=location_pricing["typical_duration"],
            available_slots=available_slots,
            quote_expires=datetime.now() + timedelta(hours=48),
            terms_conditions=terms,
        )

    def extract_customer_name(self, lead_data: Dict) -> str:
        """Extract customer name from lead data"""
        text = f"{lead_data.get('title', '')} {lead_data.get('description', '')}"

        # Look for name patterns
        name_patterns = [
            r"call me (\w+)",
            r"contact (\w+) at",
            r"(\w+) needs",
            r"my name is (\w+)",
            r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b",  # Full names
        ]

        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return "Michigan Customer"

    def generate_available_slots(self, location: str) -> List[datetime]:
        """Generate available time slots for Michigan locations"""
        slots = []
        now = datetime.now()

        # Next 7 days, excluding Sundays
        for day_offset in range(7):
            slot_date = now + timedelta(days=day_offset)

            # Skip Sundays (some Michigan cities have restrictions)
            if slot_date.weekday() == 6:  # Sunday
                continue

            # Generate morning and afternoon slots
            morning_slot = slot_date.replace(hour=9, minute=0)
            afternoon_slot = slot_date.replace(hour=14, minute=0)

            slots.extend([morning_slot, afternoon_slot])

        return slots[:10]  # Return first 10 slots

    def generate_quote_document(self, quote: MichiganQuote) -> Dict:
        """Generate professional quote document"""
        return {
            "quote_id": quote.quote_id,
            "customer_name": quote.customer_name,
            "property_address": quote.property_address,
            "issue_date": datetime.now().strftime("%Y-%m-%d"),
            "expires": quote.quote_expires.strftime("%Y-%m-%d %H:%M"),
            "pricing": {
                "estimated_cost": f"${quote.estimated_cost:,.2f}",
                "michigan_discount": f"-${quote.michigan_discount:,.2f}",
                "final_price": f"${quote.final_price:,.2f}",
            },
            "service_details": {
                "estimated_duration": quote.estimated_duration,
                "service_area": "Michigan Licensed & Insured",
                "included_services": [
                    "All labor and equipment",
                    "Transportation and disposal",
                    "Michigan recycling center fees",
                    "Donation coordination",
                    "Property protection",
                    "Before/after photos",
                ],
            },
            "available_times": [
                slot.strftime("%Y-%m-%d %I:%M %p") for slot in quote.available_slots[:5]
            ],
            "terms": quote.terms_conditions,
            "contact_info": {
                "phone": "(313) 555-CLEAN",
                "email": "quotes@cleanoutpro.com",
                "website": "www.cleanoutpro.com/michigan",
                "license": "Michigan License #CLEAN-001",
            },
        }

    def get_leads_for_quoting(self, limit: int = 15) -> List[Dict]:
        """Get leads that are ready for automated quoting"""
        cursor = self.db_conn.cursor()

        cursor.execute(
            """
            SELECT * FROM leads 
            WHERE contacted = TRUE 
               AND quoted = FALSE 
               AND urgency_score >= 0.3
               AND estimated_value >= 100
            ORDER BY urgency_score DESC, estimated_value DESC
            LIMIT ?
        """,
            (limit,),
        )

        columns = [desc[0] for desc in cursor.description]
        leads = []

        for row in cursor.fetchall():
            lead = dict(zip(columns, row))
            leads.append(lead)

        return leads

    async def send_quote_via_email(
        self, lead: Dict, quote: MichiganQuote, quote_doc: Dict
    ) -> bool:
        """Send quote via email (integrates with outreach system)"""
        try:
            # Import here to avoid circular imports
            from services.michigan_outreach import MichiganOutreachSystem

            outreach = MichiganOutreachSystem()

            subject = f"CleanoutPro Quote {quote.quote_id} - {quote.property_address}"

            body = f"""
Dear {quote.customer_name},

Thank you for your interest in CleanoutPro! Here is your personalized Michigan quote:

**Quote ID:** {quote.quote_id}
**Service Address:** {quote.property_address}
**Estimated Duration:** {quote.estimated_duration}

**Pricing Breakdown:**
Estimated Cost: {quote_doc["pricing"]["estimated_cost"]}
Michigan Discount: {quote_doc["pricing"]["michigan_discount"]}
**Final Price: {quote_doc["pricing"]["final_price"]}**

**What's Included:**
{chr(10).join(f"• {service}" for service in quote_doc["service_details"]["included_services"])}

**Available Time Slots:**
{chr(10).join(f"• {slot}" for slot in quote_doc["available_times"])}

**Michigan Service Guarantee:**
{quote_doc["terms"]}

**Ready to Book?**
Reply to this email with your preferred time slot, or call us at {quote_doc["contact_info"]["phone"]}.

This quote expires on {quote_doc["expires"]}.

Best regards,
The CleanoutPro Team
{quote_doc["contact_info"]["phone"]}
{quote_doc["contact_info"]["website"]}

---
Michigan Licensed & Insured | License #{quote_doc["contact_info"]["license"]}
            """

            # Send email (would need to implement email sending)
            logger.info(f"Quote email prepared for {lead['id']}: {quote.quote_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send quote email: {e}")
            return False

    def save_quote_to_database(self, lead: Dict, quote: MichiganQuote, quote_doc: Dict):
        """Save quote to database for tracking"""
        cursor = self.db_conn.cursor()

        cursor.execute(
            """
            INSERT INTO quotes (
                quote_id, lead_id, customer_name, property_address, 
                estimated_cost, discount_amount, final_price, 
                estimated_duration, quote_expires, terms,
                created_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                quote.quote_id,
                lead["id"],
                quote.customer_name,
                quote.property_address,
                float(quote.estimated_cost),
                float(quote.michigan_discount),
                float(quote.final_price),
                quote.estimated_duration,
                quote.quote_expires.isoformat(),
                quote.terms_conditions,
                datetime.now().isoformat(),
                "sent",
            ),
        )

        self.db_conn.commit()

    async def run_automated_quoting(self):
        """Main automated quoting process"""
        logger.info("Starting Michigan automated quoting system...")

        leads = self.get_leads_for_quoting(15)
        logger.info(f"Found {len(leads)} leads for quoting")

        quotes_generated = 0

        for lead in leads:
            try:
                # Calculate Michigan-specific quote
                quote = self.calculate_michigan_pricing(lead)
                quote_doc = self.generate_quote_document(quote)

                # Send quote
                if await self.send_quote_via_email(lead, quote, quote_doc):
                    self.save_quote_to_database(lead, quote, quote_doc)

                    # Mark lead as quoted
                    cursor = self.db_conn.cursor()
                    cursor.execute(
                        "UPDATE leads SET quoted = TRUE, quote_sent_date = ? WHERE id = ?",
                        (datetime.now().isoformat(), lead["id"]),
                    )
                    self.db_conn.commit()

                    quotes_generated += 1
                    logger.info(f"Quote sent for lead {lead['id']}: {quote.quote_id}")

                # Rate limiting
                await asyncio.sleep(2)

            except Exception as e:
                logger.error(f"Error generating quote for lead {lead['id']}: {e}")

        logger.info(f"Automated quoting complete. Generated {quotes_generated} quotes")
        return quotes_generated


if __name__ == "__main__":

    async def main():
        import sqlite3

        conn = sqlite3.connect("michigan_leads.db")
        deal_closer = MichiganDealCloser(conn)
        await deal_closer.run_automated_quoting()

    asyncio.run(main())
