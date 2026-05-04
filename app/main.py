import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging, logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    # Warm up model
    from app.services.yolo_service import yolo_service
    import numpy as np
    yolo_service.model(np.zeros((640, 640, 3), dtype=np.uint8), verbose=False)
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    logger.info(
        f"Activity: {request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration:.4f}s"
    )
    return response

# Middleware for execution timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Legacy support for root endpoints
@app.post("/detect", include_in_schema=False)
async def legacy_detect(request: Request):
    from app.api.v1.endpoints.detect import detect as detect_func
    from app.models.schemas import DetectRequest
    body = await request.json()
    return await detect_func(DetectRequest(**body))

@app.get("/health", include_in_schema=False)
async def legacy_health():
    from app.api.v1.endpoints.health import health as health_func
    return await health_func()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
