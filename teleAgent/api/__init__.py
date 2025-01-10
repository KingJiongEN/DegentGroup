from fastapi import APIRouter
from .routes import router as health_router
from .twitter_routes import router as twitter_router

# Create main API router
api_router = APIRouter(prefix="/api")

# Include all sub-routers
api_router.include_router(health_router)
api_router.include_router(twitter_router)