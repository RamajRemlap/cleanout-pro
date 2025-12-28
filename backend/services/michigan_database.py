"""
Michigan Autonomous Client Acquisition System Database Schema
Creates tables for leads, quotes, and customer interactions
"""

import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def create_michigan_database():
    """Create the complete Michigan lead generation database"""

    # Connect to SQLite database
    conn = sqlite3.connect("michigan_leads.db")
    cursor = conn.cursor()

    try:
        # Leads table - stores all scraped leads
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                price TEXT,
                location TEXT NOT NULL,
                contact_info TEXT,  -- JSON
                posted_date TEXT,
                url TEXT,
                lead_type TEXT NOT NULL,  -- 'junk_removal', 'cleanout', 'moving', 'estate'
                urgency_score REAL DEFAULT 0.0,
                estimated_value REAL DEFAULT 0.0,
                processed BOOLEAN DEFAULT FALSE,
                contacted BOOLEAN DEFAULT FALSE,
                quoted BOOLEAN DEFAULT FALSE,
                contact_date TEXT,
                quote_sent_date TEXT,
                template_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Quotes table - stores generated quotes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quote_id TEXT UNIQUE NOT NULL,
                lead_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                property_address TEXT NOT NULL,
                estimated_cost REAL NOT NULL,
                discount_amount REAL NOT NULL,
                final_price REAL NOT NULL,
                estimated_duration TEXT NOT NULL,
                quote_expires TEXT NOT NULL,
                terms TEXT,
                status TEXT DEFAULT 'sent',  -- 'sent', 'accepted', 'rejected', 'expired'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads (id)
            )
        """)

        # Customers table - stores converted customers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                lead_source TEXT,
                lead_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads (id)
            )
        """)

        # Jobs table - stores actual booked jobs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                quote_id TEXT,
                job_number TEXT UNIQUE NOT NULL,
                property_address TEXT NOT NULL,
                scheduled_date TEXT NOT NULL,
                estimated_duration TEXT,
                final_price REAL NOT NULL,
                status TEXT DEFAULT 'scheduled',  -- 'scheduled', 'in_progress', 'completed', 'cancelled'
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (quote_id) REFERENCES quotes (quote_id)
            )
        """)

        # Interactions table - tracks all customer interactions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                customer_id INTEGER,
                interaction_type TEXT NOT NULL,  -- 'email_sent', 'email_reply', 'phone_call', 'sms_sent', 'sms_reply'
                interaction_details TEXT,  -- JSON with details
                automated BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)

        # Analytics table - for performance tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metric_date TEXT NOT NULL,
                location TEXT,
                details TEXT,  -- JSON with additional context
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for performance
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_leads_urgency ON leads(urgency_score DESC)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_leads_processed ON leads(processed, contacted)"
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_leads_quoted ON leads(quoted)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_quotes_status ON quotes(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_interactions_lead ON interactions(lead_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_interactions_customer ON interactions(customer_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics(metric_date)"
        )

        # Commit all changes
        conn.commit()
        logger.info("Michigan database schema created successfully")

        # Insert sample data for testing
        insert_sample_data(cursor, conn)

        return conn

    except Exception as e:
        logger.error(f"Error creating database: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()


def insert_sample_data(cursor, conn):
    """Insert sample Michigan leads for testing"""

    sample_leads = [
        {
            "source": "facebook_marketplace",
            "title": "URGENT - Junk removal needed tomorrow",
            "description": "Need to clean out entire house before moving. Furniture, appliances, and general junk. Must be done ASAP.",
            "price": "$500",
            "location": "Detroit",
            "lead_type": "urgent_cleanout",
            "urgency_score": 0.9,
            "estimated_value": 450.0,
        },
        {
            "source": "craigslist",
            "title": "Basement cleanout - Royal Oak",
            "description": "Finished basement needs complete cleanout. Old furniture, boxes, construction debris.",
            "price": "$300",
            "location": "Royal Oak",
            "lead_type": "cleanout",
            "urgency_score": 0.4,
            "estimated_value": 350.0,
        },
        {
            "source": "facebook_marketplace",
            "title": "Estate cleanout Ann Arbor",
            "description": "Family member passed away, need to clean out entire house. Many valuable items, lots of furniture.",
            "price": "$800",
            "location": "Ann Arbor",
            "lead_type": "estate",
            "urgency_score": 0.3,
            "estimated_value": 750.0,
        },
    ]

    for lead in sample_leads:
        cursor.execute(
            """
            INSERT INTO leads (source, title, description, price, location, 
                              lead_type, urgency_score, estimated_value)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                lead["source"],
                lead["title"],
                lead["description"],
                lead["price"],
                lead["location"],
                lead["lead_type"],
                lead["urgency_score"],
                lead["estimated_value"],
            ),
        )

    conn.commit()
    logger.info(f"Inserted {len(sample_leads)} sample leads")


if __name__ == "__main__":
    # Create the database
    conn = create_michigan_database()
    print("Michigan lead generation database initialized successfully!")
    conn.close()
