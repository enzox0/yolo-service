import asyncio
import base64
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from typing import List, Optional

from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import DetectRequest, DetectResponse, Detection, BBox

COCO_CLASSES = {
    0: "person", 2: "car", 3: "motorcycle", 5: "bus", 7: "truck",
    1: "bicycle", 8: "boat", 15: "cat", 16: "dog"
}

VEHICLE_CLASSES = ["car", "bus", "truck", "motorcycle", "van", "suv", "sedan"]

class YoloService:
    def __init__(self):
        self.device = settings.DEVICE or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = YOLO(settings.MODEL_PATH).to(self.device)
        self.queue = asyncio.Queue(maxsize=settings.MAX_QUEUE_SIZE)
        self.latencies = []
        logger.info(f"YOLO Service initialized on {self.device}")

    async def predict(self, req: DetectRequest) -> DetectResponse:
        if self.queue.full():
            try:
                self.queue.get_nowait()
                logger.warning(f"Queue full for camera {req.camera_id}, dropped oldest request")
            except asyncio.QueueEmpty:
                pass
        
        await self.queue.put(req)
        start_time = time.perf_counter()
        logger.debug(f"Starting inference for camera: {req.camera_id}")
        
        try:
            # 1. Decode image
            decode_start = time.perf_counter()
            img_bytes = base64.b64decode(req.image_base64)
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                logger.error(f"Failed to decode image from camera {req.camera_id}")
                return DetectResponse(camera_id=req.camera_id, timestamp=req.timestamp, detections=[])
            
            decode_duration = (time.perf_counter() - decode_start) * 1000
            logger.debug(f"Image decoded in {decode_duration:.2f}ms")

            # 2. Run inference
            inference_start = time.perf_counter()
            results = self.model.track(
                frame, 
                tracker="bytetrack.yaml", 
                persist=True, 
                classes=list(COCO_CLASSES.keys()), 
                conf=settings.CONFIDENCE_THRESHOLD,
                verbose=False
            )
            inference_duration = (time.perf_counter() - inference_start) * 1000
            logger.debug(f"YOLO inference completed in {inference_duration:.2f}ms")
            
            detections = []
            if results and results[0].boxes:
                boxes = results[0].boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    # ROI filtering
                    if req.roi:
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        if not (req.roi.x <= center_x <= req.roi.x + req.roi.width and
                                req.roi.y <= center_y <= req.roi.y + req.roi.height):
                            continue

                    cls_id = int(box.cls[0])
                    cls_name = COCO_CLASSES.get(cls_id, "unknown")
                    
                    detection = Detection(
                        **{"class": cls_name},
                        confidence=float(box.conf[0]),
                        bbox=BBox(x=x1, y=y1, width=x2-x1, height=y2-y1),
                        track_id=int(box.id[0]) if box.id is not None else None
                    )

                    # Detailed analysis placeholders
                    if req.analyze_detailed:
                        self._enrich_detection(detection, cls_name)

                    detections.append(detection)

            # 3. Track latency
            total_duration = (time.perf_counter() - start_time) * 1000
            self.latencies.append(total_duration)
            if len(self.latencies) > settings.LATENCY_HISTORY_SIZE:
                self.latencies.pop(0)
            
            logger.info(f"Inference complete: {req.camera_id} | {len(detections)} objects | Total: {total_duration:.2f}ms")
            return DetectResponse(camera_id=req.camera_id, timestamp=req.timestamp, detections=detections)
            
        finally:
            await self.queue.get()

    def _enrich_detection(self, detection: Detection, cls_name: str):
        if cls_name in VEHICLE_CLASSES:
            detection.color = "unknown" 
            detection.vehicle_type = cls_name
        elif cls_name == "person":
            detection.attributes = {"clothing": "unknown", "action": "moving"}

    def get_p95_latency(self) -> float:
        if not self.latencies:
            return 0.0
        return float(np.percentile(self.latencies, 95))

# Global instance
yolo_service = YoloService()
