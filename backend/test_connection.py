"""Test database connection to Neon"""
from database.connection import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ Backend connected to Neon")
            print(f"✓ PostgreSQL version: {version.split(',')[0]}")

            # Count tables
            result = conn.execute(text(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
            ))
            table_count = result.fetchone()[0]
            print(f"✓ Found {table_count} tables in public schema")

            # List tables
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"
            ))
            tables = [row[0] for row in result.fetchall()]
            print(f"✓ Tables: {', '.join(tables)}")

            # Check pricing rules
            result = conn.execute(text("SELECT COUNT(*) FROM pricing_rules"))
            rules_count = result.fetchone()[0]
            print(f"✓ Pricing rules loaded: {rules_count} rules")

            print("\n✅ All connection tests passed!")
            return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
