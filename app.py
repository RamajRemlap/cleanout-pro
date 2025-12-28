"""
Root app wrapper for Railway deployment
This module makes the FastAPI app available from project root
"""
import os
import sys
from pathlib import Path

# Ensure backend is in the path
backend_dir = Path(__file__).parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

print(f"✅ Added to path: {backend_dir}")

# Load environment variables
from dotenv import load_dotenv
env_file = backend_dir / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ Loaded .env from {env_file}")
else:
    print(f"⚠️ No .env file at {env_file}")

# Import and expose the app
try:
    from api.main import app
    print("✅ FastAPI app imported successfully")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    import traceback
    traceback.print_exc()
    raise

# For Gunicorn/Uvicorn to find the app
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting server on port {port}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
