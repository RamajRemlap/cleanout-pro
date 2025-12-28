"""
Michigan Client Acquisition System
Real-time lead generation for Detroit and surrounding cities
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import re
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin, urlparse
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MichiganLead:
    """Michigan area lead data structure"""

    source: str
    title: str
    description: str
    price: Optional[str]
    location: str
    contact_info: Dict[str, str]
    posted_date: datetime
    url: str
    lead_type: str  # 'junk_removal', 'cleanout', 'moving', 'estate'
    urgency_score: float  # 0-1 based on keywords
    estimated_value: float  # estimated job value


class MichiganLeadGenerator:
    """Autonomous Michigan client acquisition system"""

    def __init__(self):
        self.cities = [
            "detroit",
            "dearborn",
            "livonia",
            "troy",
            "southfield",
            "warren",
            "sterling heights",
            "farmington hills",
            "royal oak",
            "ferndale",
            "birmingham",
            "bloomfield hills",
            "west bloomfield",
            "novi",
            "northville",
            "plymouth",
            "canton",
            "ann arbor",
            "wyandotte",
            "taylor",
            "romulus",
            "allen park",
            "melvindale",
            "river rouge",
            "ecorse",
            "lincoln park",
            "dearborn heights",
            "inkster",
            "garden city",
            "wayne",
            "westland",
        ]

        self.keywords = {
            "high_urgency": [
                "urgent",
                "asap",
                "immediately",
                "emergency",
                "must go",
                "need gone today",
                "moving tomorrow",
                "eviction",
                "foreclosure",
            ],
            "medium_urgency": [
                "moving",
                "cleanout",
                "junk removal",
                "hauling",
                "declutter",
                "estate sale",
                "garage cleanout",
                "basement cleanout",
            ],
            "junk_removal": [
                "junk",
                "trash",
                "debris",
                "waste",
                "scrap",
                "dump",
                "hauling",
                "removal",
                "cleanup",
                "dispose",
            ],
            "cleanout": [
                "cleanout",
                "clean out",
                "empty",
                "clear",
                "remove everything",
                "entire contents",
                "whole house",
                "all items",
            ],
            "moving": ["moving", "relocation", "transfer", "new job", "military"],
            "estate": [
                "estate",
                "inheritance",
                "probate",
                "deceased",
                "passed away",
                "executor",
                "attorney",
                "family member",
            ],
        }

        self.session = None
        self.db_conn = self.init_database()

    def init_database(self):
        """Initialize SQLite database for leads"""
        conn = sqlite3.connect("michigan_leads.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                title TEXT,
                description TEXT,
                price TEXT,
                location TEXT,
                contact_info TEXT,
                posted_date TEXT,
                url TEXT,
                lead_type TEXT,
                urgency_score REAL,
                estimated_value REAL,
                processed BOOLEAN DEFAULT FALSE,
                contacted BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_urgency_score ON leads(urgency_score DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_processed ON leads(processed, contacted)
        """)

        conn.commit()
        return conn

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
            timeout=aiohttp.ClientTimeout(total=30),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
        if self.db_conn:
            self.db_conn.close()

    def calculate_urgency_score(self, title: str, description: str) -> float:
        """Calculate urgency score based on keyword analysis"""
        text = (title + " " + description).lower()
        score = 0.0

        # High urgency keywords (0.4 points each)
        for keyword in self.keywords["high_urgency"]:
            if keyword in text:
                score += 0.4

        # Medium urgency keywords (0.2 points each)
        for keyword in self.keywords["medium_urgency"]:
            if keyword in text:
                score += 0.2

        # Cap at 1.0
        return min(score, 1.0)

    def classify_lead_type(self, title: str, description: str) -> str:
        """Classify lead type based on content"""
        text = (title + " " + description).lower()
        scores = {"junk_removal": 0, "cleanout": 0, "moving": 0, "estate": 0}

        for category, keywords in self.keywords.items():
            if category in scores:
                for keyword in keywords:
                    if keyword in text:
                        scores[category] += 1

        return max(scores, key=scores.get)

    def estimate_job_value(self, title: str, description: str, location: str) -> float:
        """Estimate job value based on content and location"""
        text = (title + " " + description).lower()
        base_value = 200  # Base junk removal job

        # Size indicators
        if any(word in text for word in ["house", "home", "entire", "whole"]):
            base_value += 200
        if any(word in text for word in ["apartment", "condo", "studio"]):
            base_value -= 50
        if any(word in text for word in ["basement", "garage", "shed"]):
            base_value += 100
        if any(word in text for word in ["estate", "inheritance"]):
            base_value += 300

        # Volume indicators
        if "furniture" in text:
            base_value += 75
        if "appliances" in text:
            base_value += 50
        if "construction" in text or "debris" in text:
            base_value += 150

        # Location-based pricing (Detroit metro area)
        if any(
            city in location.lower()
            for city in ["bloomfield", "birmingham", "farmington"]
        ):
            base_value *= 1.3  # Affluent areas
        elif any(city in location.lower() for city in ["detroit", "highland park"]):
            base_value *= 0.9  # Lower income areas

        return max(base_value, 100)  # Minimum $100

    async def scrape_facebook_marketplace(self) -> List[MichiganLead]:
        """Scrape Facebook Marketplace for Michigan leads"""
        leads = []

        for city in self.cities[:5]:  # Limit to major cities first
            try:
                url = f"https://www.facebook.com/marketplace/{city}/search?query=junk%20removal"
                async with self.session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")

                        # Extract listings (this is simplified - would need more sophisticated parsing)
                        listings = soup.find_all("div", class_="x78zum5")[:10]

                        for listing in listings:
                            try:
                                title_elem = listing.find("span", class_="x1lliihq")
                                title = title_elem.text if title_elem else ""

                                desc_elem = listing.find("span", class_="x1yztbdb")
                                description = desc_elem.text if desc_elem else ""

                                price_elem = listing.find("span", class_="x193iq5w")
                                price = price_elem.text if price_elem else ""

                                if title and description:
                                    leads.append(
                                        MichiganLead(
                                            source="facebook_marketplace",
                                            title=title,
                                            description=description,
                                            price=price,
                                            location=city.title(),
                                            contact_info={},  # Would need to extract from listing
                                            posted_date=datetime.now(),
                                            url=url,
                                            lead_type=self.classify_lead_type(
                                                title, description
                                            ),
                                            urgency_score=self.calculate_urgency_score(
                                                title, description
                                            ),
                                            estimated_value=self.estimate_job_value(
                                                title, description, city
                                            ),
                                        )
                                    )
                            except Exception as e:
                                logger.warning(f"Error parsing Facebook listing: {e}")

                await asyncio.sleep(1)  # Rate limiting

            except Exception as e:
                logger.error(f"Error scraping Facebook for {city}: {e}")

        return leads

    async def scrape_craigslist(self) -> List[MichiganLead]:
        """Scrape Craigslist for Michigan leads"""
        leads = []

        for city in ["detroit", "annarbor"]:
            try:
                # Search services section
                url = f"https://{city}.craigslist.org/search/svc?query=junk%20removal"
                async with self.session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")

                        listings = soup.find_all(
                            "li", class_="cl-static-search-result"
                        )[:15]

                        for listing in listings:
                            try:
                                title_elem = listing.find("a", class_="title")
                                title = title_elem.text if title_elem else ""

                                price_elem = listing.find("span", class_="price")
                                price = price_elem.text if price_elem else ""

                                # Get description from listing page
                                detail_url = (
                                    listing.find("a")["href"]
                                    if listing.find("a")
                                    else ""
                                )
                                if detail_url:
                                    try:
                                        async with self.session.get(
                                            detail_url
                                        ) as detail_response:
                                            if detail_response.status == 200:
                                                detail_html = (
                                                    await detail_response.text()
                                                )
                                                detail_soup = BeautifulSoup(
                                                    detail_html, "html.parser"
                                                )
                                                desc_elem = detail_soup.find(
                                                    "section", id="postingbody"
                                                )
                                                description = (
                                                    desc_elem.text if desc_elem else ""
                                                )
                                            else:
                                                description = ""
                                    except:
                                        description = ""

                                if title:
                                    leads.append(
                                        MichiganLead(
                                            source="craigslist",
                                            title=title,
                                            description=description,
                                            price=price,
                                            location=city.title(),
                                            contact_info={},
                                            posted_date=datetime.now(),
                                            url=detail_url,
                                            lead_type=self.classify_lead_type(
                                                title, description
                                            ),
                                            urgency_score=self.calculate_urgency_score(
                                                title, description
                                            ),
                                            estimated_value=self.estimate_job_value(
                                                title, description, city
                                            ),
                                        )
                                    )
                            except Exception as e:
                                logger.warning(f"Error parsing Craigslist listing: {e}")

                await asyncio.sleep(2)  # Rate limiting

            except Exception as e:
                logger.error(f"Error scraping Craigslist for {city}: {e}")

        return leads

    def save_leads(self, leads: List[MichiganLead]):
        """Save leads to database"""
        cursor = self.db_conn.cursor()

        for lead in leads:
            try:
                cursor.execute(
                    """
                    INSERT INTO leads (source, title, description, price, location, 
                                     contact_info, posted_date, url, lead_type, 
                                     urgency_score, estimated_value)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        lead.source,
                        lead.title,
                        lead.description,
                        lead.price,
                        lead.location,
                        json.dumps(lead.contact_info),
                        lead.posted_date.isoformat(),
                        lead.url,
                        lead.lead_type,
                        lead.urgency_score,
                        lead.estimated_value,
                    ),
                )
            except sqlite3.IntegrityError:
                logger.info(f"Lead already exists: {lead.title}")

        self.db_conn.commit()
        logger.info(f"Saved {len(leads)} leads to database")

    async def run_lead_generation(self):
        """Main lead generation loop"""
        logger.info("Starting Michigan lead generation...")

        all_leads = []

        # Scrape multiple sources
        try:
            facebook_leads = await self.scrape_facebook_marketplace()
            all_leads.extend(facebook_leads)
            logger.info(f"Found {len(facebook_leads)} Facebook leads")
        except Exception as e:
            logger.error(f"Facebook scraping error: {e}")

        try:
            craigslist_leads = await self.scrape_craigslist()
            all_leads.extend(craigslist_leads)
            logger.info(f"Found {len(craigslist_leads)} Craigslist leads")
        except Exception as e:
            logger.error(f"Craigslist scraping error: {e}")

        # Save to database
        self.save_leads(all_leads)

        # Get top high-urgency leads
        cursor = self.db_conn.cursor()
        cursor.execute("""
            SELECT * FROM leads 
            WHERE processed = FALSE AND urgency_score >= 0.6
            ORDER BY urgency_score DESC, estimated_value DESC 
            LIMIT 10
        """)

        top_leads = cursor.fetchall()
        logger.info(f"Top {len(top_leads)} high-urgency leads ready for contact")

        return all_leads, top_leads


if __name__ == "__main__":

    async def main():
        async with MichiganLeadGenerator() as generator:
            await generator.run_lead_generation()

    asyncio.run(main())
