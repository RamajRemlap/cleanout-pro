"""
CleanoutPro Backend - Root Entry Point
This is the main entry point for Railway and other cloud deployments
"""
import os
import sys
from pathlib import Path

# Ensure backend directory is in Python path
backend_path = Path(__file__).parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

# Load environment variables from backend/.env
from dotenv import load_dotenv
env_file = backend_path / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ Environment loaded from {env_file}")
else:
    print(f"ℹ️  No .env file at {env_file}, using Railway variables")

# Import the FastAPI app
print("📦 Importing CleanoutPro API...")
try:
    from api.main import app
    print("✅ CleanoutPro API imported successfully")
except ImportError as e:
    print(f"❌ Failed to import FastAPI app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Expose for ASGI servers
__all__ = ["app"]

# Run directly if invoked as main
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting CleanoutPro API on http://0.0.0.0:{port}")
    print(f"📚 API docs available at http://0.0.0.0:{port}/docs")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True
    )

