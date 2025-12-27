"""
Helper script to set up Neon database connection
"""

import os
import sys
from pathlib import Path

def update_env_file(connection_string):
    """Update .env file with Neon connection string"""
    env_path = Path(__file__).parent / ".env"

    if not env_path.exists():
        print("[ERROR] .env file not found!")
        return False

    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()

    # Update DATABASE_URL line
    updated_lines = []
    found = False
    for line in lines:
        if line.startswith('DATABASE_URL='):
            updated_lines.append(f'DATABASE_URL={connection_string}\n')
            found = True
        else:
            updated_lines.append(line)

    if not found:
        updated_lines.append(f'\nDATABASE_URL={connection_string}\n')

    # Write updated .env
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)

    print(f"[OK] Updated .env file with Neon connection string")
    return True


def test_connection(connection_string):
    """Test PostgreSQL connection"""
    print("\n[TEST] Testing database connection...")

    try:
        from sqlalchemy import create_engine, text

        engine = create_engine(connection_string)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"[OK] Connected successfully!")
            print(f"     PostgreSQL version: {version.split(',')[0]}")
            return True

    except ImportError:
        print("[ERROR] SQLAlchemy not installed. Run: pip install sqlalchemy psycopg2-binary")
        return False
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False


def main():
    print("=" * 70)
    print("Neon Database Setup - CleanoutPro")
    print("=" * 70)

    print("\n[STEP 1] Create Neon Account")
    print("   1. Go to: https://console.neon.tech/signup")
    print("   2. Sign up with GitHub (fastest) or email")
    print("   3. Verify your email if required")

    print("\n[STEP 2] Create Project")
    print("   1. Click 'Create a project' or 'New Project'")
    print("   2. Project name: cleanoutpro")
    print("   3. Database name: cleanoutpro")
    print("   4. Region: Choose closest to you")
    print("   5. Click 'Create project'")

    print("\n[STEP 3] Get Connection String")
    print("   1. In your project dashboard, find 'Connection Details'")
    print("   2. Select 'Pooled connection' (recommended)")
    print("   3. Copy the connection string")
    print("   4. It looks like:")
    print("      postgresql://user:password@ep-xxx.region.aws.neon.tech/cleanoutpro")

    print("\n" + "=" * 70)
    print("Paste your Neon connection string below:")
    print("(or press Enter to skip and update .env manually)")
    print("=" * 70)

    connection_string = input("\nConnection string: ").strip()

    if not connection_string:
        print("\n[WARNING] No connection string provided.")
        print(f"          Update manually in: backend/.env")
        print(f"          Line: DATABASE_URL=your_connection_string")
        return

    # Validate format
    if not connection_string.startswith('postgresql://'):
        print("\n[ERROR] Invalid format. Should start with: postgresql://")
        return

    # Update .env
    if update_env_file(connection_string):
        # Test connection
        if test_connection(connection_string):
            print("\n" + "=" * 70)
            print("[SUCCESS] DATABASE SETUP COMPLETE!")
            print("=" * 70)
            print("\nNext steps:")
            print("   1. Create tables and test data:")
            print("      python create_test_data.py")
            print("\n   2. Test API at:")
            print("      http://localhost:8001/docs")
            print()
        else:
            print("\n[WARNING] Connection test failed. Check your connection string.")


if __name__ == "__main__":
    main()
