from fastapi import APIRouter
from .endpoints.detect import router as detect_router
from .endpoints.health import router as health_router

api_router = APIRouter()
api_router.include_router(detect_router, prefix="/detect", tags=["detection"])
api_router.include_router(health_router, prefix="/health", tags=["system"])
