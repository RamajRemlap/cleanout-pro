"""
Quick database connection test
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 60)
print("DATABASE CONNECTION TEST")
print("=" * 60)

print(f"\nDatabase URL: {DATABASE_URL[:50]}...")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)

    # Test connection
    with engine.connect() as conn:
        # Get PostgreSQL version
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"\n[OK] Connection successful!")
        print(f"\nPostgreSQL Version:\n{version[:100]}...")

        # Check tables
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]

        print(f"\nTables in database ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")

        # Check pricing rules
        result = conn.execute(text("SELECT COUNT(*) FROM pricing_rules"))
        rule_count = result.fetchone()[0]
        print(f"\nPricing rules configured: {rule_count}")

        # Check if there are any jobs
        result = conn.execute(text("SELECT COUNT(*) FROM jobs"))
        job_count = result.fetchone()[0]
        print(f"Jobs in database: {job_count}")

        # Check if there are any customers
        result = conn.execute(text("SELECT COUNT(*) FROM customers"))
        customer_count = result.fetchone()[0]
        print(f"Customers in database: {customer_count}")

    print("\n" + "=" * 60)
    print("[OK] DATABASE READY FOR USE")
    print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] Connection failed: {e}")
    print("\nTroubleshooting:")
    print("   1. Check DATABASE_URL in .env file")
    print("   2. Verify Neon project is active")
    print("   3. Check internet connection")
    exit(1)
