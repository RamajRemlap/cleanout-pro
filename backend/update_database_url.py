"""
Quick script to update DATABASE_URL in .env file
Usage: python update_database_url.py "your_connection_string_here"
"""

import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("=" * 70)
    print("Update Database Connection String")
    print("=" * 70)
    print("\nUsage:")
    print('  python update_database_url.py "postgresql://user:pass@host/db"')
    print("\nOr edit .env file manually:")
    print("  1. Open: backend/.env")
    print("  2. Update line: DATABASE_URL=your_connection_string")
    print()
    sys.exit(1)

connection_string = sys.argv[1]

# Validate format
if not connection_string.startswith('postgresql://'):
    print("[ERROR] Invalid format. Must start with: postgresql://")
    sys.exit(1)

# Update .env
env_path = Path(__file__).parent / ".env"

if not env_path.exists():
    print("[ERROR] .env file not found at:", env_path)
    sys.exit(1)

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
        print(f"[OK] Updated DATABASE_URL")
    else:
        updated_lines.append(line)

if not found:
    updated_lines.append(f'\nDATABASE_URL={connection_string}\n')
    print(f"[OK] Added DATABASE_URL")

# Write updated .env
with open(env_path, 'w') as f:
    f.writelines(updated_lines)

print(f"[OK] Saved to: {env_path}")

# Test connection
print("\n[TEST] Testing connection...")
try:
    from sqlalchemy import create_engine, text
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.scalar()
        print(f"[SUCCESS] Connected to PostgreSQL!")
        print(f"          Version: {version.split(',')[0]}")
        print("\nNext step:")
        print("  python create_test_data.py")
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    print("\nCheck your connection string and try again.")
