"""
TabDrop Backend API - FastAPI application entry point
"""
from fastapi import FastAPI
from app.config import settings
from app.core.middleware import setup_middleware
from app.api.router import api_router


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for TabDrop - Send links from phone to desktop",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup middleware (CORS, etc.)
setup_middleware(app)

# Include all API routes
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "TabDrop API is running", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (dev only)
    )