from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services.yolo_service import yolo_service
from app.core.config import settings

router = APIRouter()

@router.get("", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok" if yolo_service.queue.qsize() < (settings.MAX_QUEUE_SIZE * 0.8) else "degraded",
        model="yolo11n",
        device=str(yolo_service.device),
        queue_depth=yolo_service.queue.qsize(),
        p95_latency_ms=yolo_service.get_p95_latency()
    )
