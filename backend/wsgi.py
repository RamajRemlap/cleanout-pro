"""
WSGI entry point for Railway/Heroku deployment
This file ensures the app can be started from the project root
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

print(f"📁 Backend path: {backend_path}")
print(f"📁 Python path: {sys.path[0]}")

# Load environment
try:
    from dotenv import load_dotenv
    env_file = backend_path / ".env"
    print(f"📄 Loading .env from: {env_file}")
    load_dotenv(dotenv_path=env_file, override=False)
    print("✅ Environment loaded")
except Exception as e:
    print(f"⚠️ Warning loading .env: {e}")

# Import app
try:
    from api.main import app
    print("✅ App imported successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Export for WSGI servers
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting uvicorn on port {port}")
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
