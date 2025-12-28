"""
Vercel serverless entry point for CleanoutPro FastAPI
Vercel requires ASGI app to be exported directly
"""
import os
import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

print("🔧 Vercel serverless initializing...")

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded")
except Exception as e:
    print(f"⚠️ Warning loading .env: {e}")

# Import and expose FastAPI app
try:
    from api.main import app
    print("✅ FastAPI app imported successfully")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    import traceback
    traceback.print_exc()
    raise

# Export ASGI app for Vercel
# Vercel looks for a variable named 'app' or a function named 'handler'
__all__ = ["app"]
