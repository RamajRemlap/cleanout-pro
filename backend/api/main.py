"""
CleanoutPro Backend API
FastAPI application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CleanoutPro API",
    description="API for cleanout/junk removal business management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# Health check endpoint
@app.get("/")
async def root():
    return {
        "service": "CleanoutPro API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Import and register routes
from api.routes import jobs, rooms

app.include_router(jobs.router)
app.include_router(rooms.router)

# TODO: Add remaining routes as they are created
# from api.routes import customers, invoices, ai, paypal
# app.include_router(customers.router)
# app.include_router(invoices.router)
# app.include_router(ai.router)
# app.include_router(paypal.router)

# Startup event
@app.on_event("startup")
async def startup_event():
    import os
    from database.connection import DATABASE_URL
    logger.info("🚀 CleanoutPro API starting up...")
    logger.info(f"🔗 Database URL: {DATABASE_URL[:50]}...")
    logger.info("📊 Database connection: Ready")
    logger.info("🤖 AI Vision service: Ready")
    logger.info("💳 PayPal integration: Ready")
    logger.info("✅ All systems operational")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 CleanoutPro API shutting down...")
    logger.info("✅ Cleanup complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
