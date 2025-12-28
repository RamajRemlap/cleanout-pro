"""
Michigan Autonomous Client Acquisition Orchestrator
Runs the complete client acquisition pipeline automatically
"""

import asyncio
import logging
from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List
import json
import os

# Import Michigan services
from services.michigan_database import create_michigan_database
from services.michigan_lead_generator import MichiganLeadGenerator
from services.michigan_outreach import MichiganOutreachSystem
from services.michigan_deal_closer import MichiganDealCloser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("michigan_autonomous.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class MichiganAutonomousSystem:
    """Main orchestrator for autonomous Michigan client acquisition"""

    def __init__(self):
        self.db_conn = create_michigan_database()
        self.is_running = False
        self.stats = {
            "leads_found": 0,
            "leads_contacted": 0,
            "quotes_sent": 0,
            "deals_closed": 0,
            "revenue_generated": 0.0,
        }

        # Michigan business hours (avoid early morning/late night outreach)
        self.business_hours = {
            "start_hour": 8,  # 8 AM
            "end_hour": 19,  # 7 PM
            "weekend_work": False,  # Skip weekends for automated outreach
        }

    def is_business_hours(self) -> bool:
        """Check if current time is within Michigan business hours"""
        now = datetime.now()
        current_hour = now.hour
        is_weekday = now.weekday() < 5  # Monday-Friday

        if not is_weekday and not self.business_hours["weekend_work"]:
            return False

        return (
            self.business_hours["start_hour"]
            <= current_hour
            <= self.business_hours["end_hour"]
        )

    async def run_lead_generation(self):
        """Run lead generation phase"""
        logger.info("🔍 Starting Michigan lead generation...")

        try:
            async with MichiganLeadGenerator() as generator:
                all_leads, top_leads = await generator.run_lead_generation()

                self.stats["leads_found"] += len(all_leads)
                logger.info(
                    f"✅ Found {len(all_leads)} total leads, {len(top_leads)} high-urgency leads"
                )

                return len(all_leads) > 0

        except Exception as e:
            logger.error(f"❌ Lead generation failed: {e}")
            return False

    async def run_outreach_campaign(self):
        """Run outreach campaign phase"""
        if not self.is_business_hours():
            logger.info("⏰ Outside business hours, skipping outreach")
            return False

        logger.info("📧 Starting Michigan outreach campaign...")

        try:
            outreach_system = MichiganOutreachSystem()
            contacts_made = await outreach_system.run_outreach_campaign()

            self.stats["leads_contacted"] += contacts_made
            logger.info(f"✅ Contacted {contacts_made} leads")

            return contacts_made > 0

        except Exception as e:
            logger.error(f"❌ Outreach campaign failed: {e}")
            return False

    async def run_deal_closing(self):
        """Run deal closing phase"""
        logger.info("💰 Starting Michigan deal closing...")

        try:
            deal_closer = MichiganDealCloser(self.db_conn)
            quotes_generated = await deal_closer.run_automated_quoting()

            self.stats["quotes_sent"] += quotes_generated
            logger.info(f"✅ Generated {quotes_generated} quotes")

            return quotes_generated > 0

        except Exception as e:
            logger.error(f"❌ Deal closing failed: {e}")
            return False

    def update_analytics(self):
        """Update performance analytics"""
        cursor = self.db_conn.cursor()

        # Record daily metrics
        metrics = [
            (
                "leads_found_today",
                self.stats["leads_found"],
                datetime.now().strftime("%Y-%m-%d"),
            ),
            (
                "leads_contacted_today",
                self.stats["leads_contacted"],
                datetime.now().strftime("%Y-%m-%d"),
            ),
            (
                "quotes_sent_today",
                self.stats["quotes_sent"],
                datetime.now().strftime("%Y-%m-%d"),
            ),
            (
                "revenue_today",
                self.stats["revenue_generated"],
                datetime.now().strftime("%Y-%m-%d"),
            ),
        ]

        for metric_name, value, date in metrics:
            cursor.execute(
                """
                INSERT INTO analytics (metric_name, metric_value, metric_date, details)
                VALUES (?, ?, ?, ?)
            """,
                (metric_name, value, date, json.dumps(self.stats)),
            )

        self.db_conn.commit()
        logger.info("📊 Analytics updated")

    def generate_daily_report(self) -> str:
        """Generate daily performance report"""
        report = f"""
🚀 MICHIGAN AUTONOMOUS CLIENT ACQUISITION REPORT
{"=" * 60}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
System Status: {"🟢 ACTIVE" if self.is_running else "🔴 STOPPED"}

📈 TODAY'S PERFORMANCE:
• Leads Found: {self.stats["leads_found"]}
• Leads Contacted: {self.stats["leads_contacted"]}
• Quotes Sent: {self.stats["quotes_sent"]}
• Deals Closed: {self.stats["deals_closed"]}
• Revenue Generated: ${self.stats["revenue_generated"]:,.2f}

🎯 CONVERSION RATES:
• Contact Rate: {(self.stats["leads_contacted"] / max(self.stats["leads_found"], 1) * 100):.1f}%
• Quote Rate: {(self.stats["quotes_sent"] / max(self.stats["leads_contacted"], 1) * 100):.1f}%
• Close Rate: {(self.stats["deals_closed"] / max(self.stats["quotes_sent"], 1) * 100):.1f}%

💰 BUSINESS INSIGHTS:
• Average Deal Value: ${self.stats["revenue_generated"] / max(self.stats["deals_closed"], 1):,.2f}
• Lead Quality Score: {sum([self.stats["leads_found"], self.stats["leads_contacted"], self.stats["quotes_sent"]]) / 3:.1f}

📋 NEXT ACTIONS:
• {"Continue normal operations" if self.is_running else "Restart system"}
• Monitor conversion rates
• Optimize outreach templates
• Expand Michigan coverage area

{"=" * 60}
        """.strip()

        return report

    def save_daily_report(self, report: str):
        """Save daily report to file"""
        filename = f"michigan_report_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(filename, "w") as f:
            f.write(report)
        logger.info(f"📄 Daily report saved: {filename}")

    async def run_autonomous_cycle(self):
        """Run complete autonomous cycle"""
        logger.info("🚀 Starting autonomous Michigan client acquisition cycle...")

        cycle_success = True

        # Phase 1: Lead Generation
        cycle_success &= await self.run_lead_generation()
        await asyncio.sleep(5)  # Brief pause between phases

        # Phase 2: Outreach (business hours only)
        if self.is_business_hours():
            cycle_success &= await self.run_outreach_campaign()
            await asyncio.sleep(5)

        # Phase 3: Deal Closing
        cycle_success &= await self.run_deal_closing()

        # Phase 4: Analytics & Reporting
        self.update_analytics()
        report = self.generate_daily_report()
        self.save_daily_report(report)

        logger.info(f"✅ Autonomous cycle completed. Success: {cycle_success}")
        print(report)  # Also print to console

        return cycle_success

    async def start_autonomous_mode(self):
        """Start continuous autonomous operation"""
        self.is_running = True
        logger.info("🤖 Michigan Autonomous System STARTED")

        # Run immediately on start
        await self.run_autonomous_cycle()

        # Then run every 30 minutes
        while self.is_running:
            try:
                await asyncio.sleep(30 * 60)  # 30 minutes between cycles

                if not self.is_running:
                    break

                logger.info("🔄 Starting new autonomous cycle...")
                await self.run_autonomous_cycle()

            except KeyboardInterrupt:
                logger.info("🛑 Received interrupt signal, stopping...")
                break
            except Exception as e:
                logger.error(f"❌ Error in autonomous cycle: {e}")
                # Continue running even if cycle fails

        self.is_running = False
        logger.info("🛑 Michigan Autonomous System STOPPED")

    def stop_autonomous_mode(self):
        """Stop autonomous operation"""
        self.is_running = False
        logger.info("🛑 Stop signal sent to Michigan Autonomous System")

    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            "running": self.is_running,
            "business_hours": self.is_business_hours(),
            "stats": self.stats,
            "last_update": datetime.now().isoformat(),
        }


# Command line interface
async def main():
    """Main entry point"""
    import sys

    orchestrator = MichiganAutonomousSystem()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "start":
            logger.info("🚀 Starting Michigan Autonomous Client Acquisition System")
            await orchestrator.start_autonomous_mode()
        elif command == "once":
            logger.info("🔍 Running single autonomous cycle")
            await orchestrator.run_autonomous_cycle()
        elif command == "status":
            status = orchestrator.get_system_status()
            print(json.dumps(status, indent=2))
        else:
            print("Usage: python michigan_autonomous.py [start|once|status]")
    else:
        # Default: run one cycle
        await orchestrator.run_autonomous_cycle()


if __name__ == "__main__":
    asyncio.run(main())
