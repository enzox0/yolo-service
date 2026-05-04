from fastapi import APIRouter, HTTPException
from app.models.schemas import DetectRequest, DetectResponse
from app.services.yolo_service import yolo_service
from app.core.logging import logger

router = APIRouter()

@router.post("", response_model=DetectResponse)
async def detect(req: DetectRequest):
    try:
        return await yolo_service.predict(req)
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during inference")
