"""
Michigan Client Outreach and Deal Closing System
Automated email/SMS outreach with Michigan-specific messaging
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random
import re
from twilio.rest import Client as TwilioClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class OutreachTemplate:
    """Michigan-specific outreach template"""

    name: str
    subject: str
    body_template: str
    type: str  # 'email', 'sms'
    urgency_appropriate: bool
    estimated_response_rate: float


class MichiganOutreachSystem:
    """Automated outreach system for Michigan leads"""

    def __init__(self):
        self.db_conn = sqlite3.connect("michigan_leads.db", check_same_thread=False)
        self.smtp_config = {
            "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "port": int(os.getenv("SMTP_PORT", "587")),
            "username": os.getenv("SMTP_USERNAME"),
            "password": os.getenv("SMTP_PASSWORD"),
            "from_email": os.getenv("FROM_EMAIL", "quotes@cleanoutpro.com"),
        }

        self.twilio_config = {
            "account_sid": os.getenv("TWILIO_ACCOUNT_SID"),
            "auth_token": os.getenv("TWILIO_AUTH_TOKEN"),
            "from_number": os.getenv("TWILIO_FROM_NUMBER"),
        }

        self.templates = self.load_michigan_templates()

        # Michigan area knowledge for personalization
        self.area_info = {
            "detroit": {
                "nickname": "Motor City",
                "major_employers": ["Ford", "GM", "Stellantis", "Quicken Loans"],
                "common_needs": [
                    "eviction cleanouts",
                    "renovation debris",
                    "foreclosure cleanouts",
                ],
            },
            "ann_arbor": {
                "nickname": "A2",
                "major_employers": ["University of Michigan", "Michigan Medicine"],
                "common_needs": ["student housing cleanouts", "faculty moves"],
            },
            "royal_oak": {
                "nickname": "Royal Oak",
                "common_needs": ["downtown business cleanouts", "home renovations"],
            },
        }

    def load_michigan_templates(self) -> List[OutreachTemplate]:
        """Load Michigan-specific outreach templates"""
        return [
            OutreachTemplate(
                name="urgent_detroit_eviction",
                subject="🚨 Urgent Junk Removal - Detroit Area - Same Day Service Available",
                body_template="""
Hi {contact_name},

I saw your listing about {listing_title} in {location}. 

We specialize in URGENT cleanouts and junk removal here in the Detroit area. Whether it's an eviction, foreclosure, or emergency cleanup - we can help TODAY.

🚚 **Same-Day Service Available**
💰 **Competitive Detroit Pricing**
🏠 **Fully Licensed & Insured**
⏰ **24/7 Emergency Service**

Detroit locals trust us because:
• We know Motor City properties (from downtown condos to suburban homes)
• We handle Detroit-specific cleanouts (evictions, renovations, foreclosures)
• We're fast - most jobs completed in 2-4 hours
• We recycle and donate when possible (good for our community)

**Quick Quote**: {estimated_price}

Can I call you in the next hour to discuss details? Or reply with the best time to reach you.

Your Detroit neighbors,
CleanoutPro Team
{phone_number}
{website}
                """,
                type="email",
                urgency_appropriate=True,
                estimated_response_rate=0.45,
            ),
            OutreachTemplate(
                name="michigan_standard_cleanout",
                subject="Professional Junk Removal Quote for {location} Area",
                body_template="""
Hello {contact_name},

I came across your post about {listing_title} in {location}.

CleanoutPro is Michigan's trusted junk removal service. We've helped thousands of homeowners across Metro Detroit, Ann Arbor, and surrounding areas.

**Why Michigan Chooses Us:**
✅ **Local Knowledge** - We know {area_nickname} properties inside and out
✅ **Fair Pricing** - No hidden fees, just honest Michigan work
✅ **Fast Service** - Most jobs completed same or next day
✅ **Eco-Friendly** - We donate usable items to Michigan charities

**Your Project Estimate**: {estimated_price}
This includes labor, transportation, and disposal fees.

Our services include:
• Complete house/apartment cleanouts
• Furniture, appliances, and electronics removal
• Construction debris and renovation cleanup
• Storage unit cleanouts
• Estate and inheritance cleanouts

Ready to get started? Reply to this email or call us at {phone_number} for a free, no-obligation consultation.

Proudly serving Michigan communities,
CleanoutPro Team
{phone_number}
{website}
                """,
                type="email",
                urgency_appropriate=False,
                estimated_response_rate=0.25,
            ),
            OutreachTemplate(
                name="sms_urgent_michigan",
                body_template="""
CleanoutPro: Saw your post about {listing_title}. We offer SAME-DAY junk removal in {location}. Quick quote: ${estimated_price}. Call {phone_number} ASAP! Fast, reliable Michigan service.
                """,
                type="sms",
                urgency_appropriate=True,
                estimated_response_rate=0.35,
            ),
            OutreachTemplate(
                name="sms_standard_michigan",
                body_template="""
CleanoutPro: Professional junk removal for your {listing_title} in {location}. Estimate: ${estimated_price}. Fully licensed Michigan company. Call {phone_number} for free quote!
                """,
                type="sms",
                urgency_appropriate=False,
                estimated_response_rate=0.20,
            ),
        ]

    def get_area_info(self, location: str) -> Dict:
        """Get area-specific information for personalization"""
        location_lower = location.lower()
        for area, info in self.area_info.items():
            if area in location_lower:
                return info
        return {"nickname": location, "major_employers": [], "common_needs": []}

    def personalize_message(self, template: OutreachTemplate, lead_data: Dict) -> str:
        """Personalize outreach message with Michigan-specific content"""
        area_info = self.get_area_info(lead_data.get("location", ""))

        # Extract contact name from listing if possible
        contact_name = self.extract_contact_name(lead_data.get("description", ""))
        if not contact_name:
            contact_name = "Homeowner"

        # Format price with Michigan-appropriate pricing
        price = self.format_price(lead_data.get("estimated_value", 0))

        # Personalization variables
        replacements = {
            "{contact_name}": contact_name,
            "{listing_title}": lead_data.get("title", "your project"),
            "{location}": lead_data.get("location", "your area"),
            "{area_nickname}": area_info["nickname"],
            "{estimated_price}": price,
            "{phone_number}": "(313) 555-CLEAN",  # Michigan area code
            "{website}": "www.cleanoutpro.com/michigan",
        }

        # Replace template variables
        message = template.body_template
        for placeholder, value in replacements.items():
            message = message.replace(placeholder, value)

        return message

    def extract_contact_name(self, text: str) -> Optional[str]:
        """Extract contact name from listing text"""
        # Look for name patterns like "My name is John" or "Contact Sarah"
        name_patterns = [
            r"my name is (\w+)",
            r"contact (\w+)",
            r"call me at.*?(\w+)",
            r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b",  # Full names
        ]

        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return None

    def format_price(self, estimated_value: float) -> str:
        """Format price with Michigan-specific messaging"""
        base_price = int(estimated_value)

        # Add Michigan-specific pricing tiers
        if base_price < 200:
            return f"${base_price} (Michigan Minimum - Small Job Special)"
        elif base_price < 400:
            return f"${base_price} (Detroit Metro Standard)"
        else:
            return f"${base_price} (Complete Property Cleanout)"

    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send personalized email"""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_config["from_email"]
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(self.smtp_config["server"], self.smtp_config["port"])
            server.starttls()
            server.login(self.smtp_config["username"], self.smtp_config["password"])
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    async def send_sms(self, to_number: str, message: str) -> bool:
        """Send SMS message via Twilio"""
        try:
            if not self.twilio_config["account_sid"]:
                logger.warning("Twilio not configured, skipping SMS")
                return False

            client = TwilioClient(
                self.twilio_config["account_sid"], self.twilio_config["auth_token"]
            )

            message = client.messages.create(
                body=message, from_=self.twilio_config["from_number"], to=to_number
            )

            logger.info(f"SMS sent to {to_number}: {message.sid}")
            return True

        except Exception as e:
            logger.error(f"Failed to send SMS to {to_number}: {e}")
            return False

    def select_best_template(self, lead_data: Dict) -> OutreachTemplate:
        """Select the best template based on lead characteristics"""
        urgency_score = lead_data.get("urgency_score", 0)
        lead_type = lead_data.get("lead_type", "")

        # Filter templates by appropriateness
        appropriate_templates = [
            t
            for t in self.templates
            if (urgency_score >= 0.6 and t.urgency_appropriate)
            or (urgency_score < 0.6 and not t.urgency_appropriate)
        ]

        # If no appropriate templates, use all
        if not appropriate_templates:
            appropriate_templates = self.templates

        # Select based on lead type and response rate
        if lead_type == "estate":
            estate_templates = [
                t for t in appropriate_templates if "professional" in t.name.lower()
            ]
            if estate_templates:
                return random.choice(estate_templates)

        # Return highest response rate template
        return max(appropriate_templates, key=lambda t: t.estimated_response_rate)

    def get_high_quality_leads(self, limit: int = 20) -> List[Dict]:
        """Get high-quality leads for outreach"""
        cursor = self.db_conn.cursor()

        cursor.execute(
            """
            SELECT * FROM leads 
            WHERE processed = FALSE 
               AND contacted = FALSE 
               AND urgency_score >= 0.4
               AND estimated_value >= 150
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

    async def run_outreach_campaign(self):
        """Main outreach campaign execution"""
        logger.info("Starting Michigan outreach campaign...")

        leads = self.get_high_quality_leads(20)
        logger.info(f"Found {len(leads)} leads for outreach")

        successful_contacts = 0

        for lead in leads:
            try:
                # Select best template
                template = self.select_best_template(lead)

                # Personalize message
                message = self.personalize_message(template, lead)

                # Extract contact information (would need more sophisticated parsing)
                contact_info = json.loads(lead.get("contact_info", "{}"))
                email = contact_info.get("email")
                phone = contact_info.get("phone")

                # Send message
                contact_success = False
                if template.type == "email" and email:
                    subject = template.subject.format(
                        **{
                            "location": lead.get("location", "Michigan"),
                            "listing_title": lead.get("title", "your project"),
                        }
                    )
                    contact_success = await self.send_email(email, subject, message)

                elif template.type == "sms" and phone:
                    contact_success = await self.send_sms(phone, message)

                # Mark as contacted
                if contact_success:
                    self.mark_lead_contacted(lead["id"], template.name)
                    successful_contacts += 1
                    logger.info(f"Successfully contacted lead {lead['id']}")

                # Rate limiting
                await asyncio.sleep(random.uniform(2, 5))

            except Exception as e:
                logger.error(f"Error processing lead {lead['id']}: {e}")

        logger.info(
            f"Outreach campaign complete. Contacted {successful_contacts}/{len(leads)} leads"
        )
        return successful_contacts

    def mark_lead_contacted(self, lead_id: int, template_used: str):
        """Mark lead as contacted in database"""
        cursor = self.db_conn.cursor()
        cursor.execute(
            """
            UPDATE leads 
            SET contacted = TRUE, 
                processed = TRUE,
                contact_date = ?,
                template_used = ?
            WHERE id = ?
        """,
            (datetime.now().isoformat(), template_used, lead_id),
        )
        self.db_conn.commit()


if __name__ == "__main__":

    async def main():
        outreach_system = MichiganOutreachSystem()
        await outreach_system.run_outreach_campaign()

    asyncio.run(main())
