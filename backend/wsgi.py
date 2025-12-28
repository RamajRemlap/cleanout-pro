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

# Load environment
from dotenv import load_dotenv
load_dotenv(dotenv_path=backend_path / ".env")

# Import app
try:
    from api.main import app
    print("✅ App imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Export for WSGI servers
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
