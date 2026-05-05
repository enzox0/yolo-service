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
from app.services.analyzers.color_analyzer import color_analyzer
from app.services.analyzers.plate_analyzer import plate_analyzer

COCO_CLASSES = {
    0: "person", 2: "car", 3: "motorcycle", 5: "bus", 7: "truck",
    1: "bicycle", 8: "boat", 15: "cat", 16: "dog"
}

VEHICLE_CLASSES = ["car", "bus", "truck", "motorcycle", "van", "suv", "sedan"]

class CentroidTracker:
    def __init__(self, max_disappeared=3):
        self.next_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared

    def register(self, centroid):
        self.objects[self.next_id] = centroid
        self.disappeared[self.next_id] = 0
        self.next_id += 1
        return self.next_id - 1

    def deregister(self, obj_id):
        del self.objects[obj_id]
        del self.disappeared[obj_id]

    def update(self, rects):
        if len(rects) == 0:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)
            return {} # Return empty mapping for no rects

        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (x, y, w, h)) in enumerate(rects):
            cX = int(x + (w / 2.0))
            cY = int(y + (h / 2.0))
            input_centroids[i] = (cX, cY)

        if len(self.objects) == 0:
            ids = []
            for i in range(0, len(input_centroids)):
                ids.append(self.register(input_centroids[i]))
            return {i: ids[i] for i in range(len(ids))}
        else:
            obj_ids = list(self.objects.keys())
            obj_centroids = list(self.objects.values())

            D = np.linalg.norm(np.array(obj_centroids)[:, np.newaxis] - input_centroids, axis=2)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()
            
            # Mapping from input_centroid index to object ID
            mapping = {}

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                # If distance is too far, don't match (especially for 4s intervals)
                if D[row, col] > 300: # Threshold in pixels
                    continue

                obj_id = obj_ids[row]
                self.objects[obj_id] = input_centroids[col]
                self.disappeared[obj_id] = 0
                used_rows.add(row)
                used_cols.add(col)
                mapping[col] = obj_id

            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)

            for row in unused_rows:
                obj_id = obj_ids[row]
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)

            for col in unused_cols:
                mapping[col] = self.register(input_centroids[col])

            return mapping

class YoloService:
    def __init__(self):
        self.device = settings.DEVICE or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = YOLO(settings.MODEL_PATH).to(self.device)
        self.queue = asyncio.Queue(maxsize=settings.MAX_QUEUE_SIZE)
        self.latencies = []
        # Per-camera trackers
        self.trackers = {} 
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
        
        try:
            # 1. Decode and pre-process image
            img_bytes = base64.b64decode(req.image_base64)
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                logger.error(f"Failed to decode image from camera {req.camera_id}")
                return DetectResponse(camera_id=req.camera_id, timestamp=req.timestamp, detections=[])

            # Downscale if larger than 640px for massive speedup on CPU
            h, w = frame.shape[:2]
            max_dim = max(h, w)
            scale = 1.0
            if max_dim > 640:
                scale = 640 / max_dim
                # Use INTER_AREA for downscaling (better quality)
                proc_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            else:
                proc_frame = frame
            
            # 2. Run inference in a thread to keep event loop free
            # Use imgsz=640 for consistency and speed
            # Use half=True if on GPU
            results = await asyncio.to_thread(
                self.model.predict,
                proc_frame,
                classes=list(COCO_CLASSES.keys()),
                conf=settings.CONFIDENCE_THRESHOLD * 0.8,
                verbose=False,
                imgsz=640,
                half=(self.device == "cuda")
            )
            
            detections = []
            rects = []
            raw_detections = []

            if results and results[0].boxes:
                boxes = results[0].boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    # Rescale coordinates back to original frame size
                    if scale != 1.0:
                        x1, y1, x2, y2 = x1/scale, y1/scale, x2/scale, y2/scale

                    # ROI filtering
                    if req.roi:
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        if not (req.roi.x <= center_x <= req.roi.x + req.roi.width and
                                req.roi.y <= center_y <= req.roi.y + req.roi.height):
                            continue

                    cls_id = int(box.cls[0])
                    cls_name = COCO_CLASSES.get(cls_id, "unknown")
                    
                    # Store for tracking
                    rects.append((x1, y1, x2-x1, y2-y1))
                    raw_detections.append({
                        "class": cls_name,
                        "confidence": float(box.conf[0]),
                        "bbox": BBox(x=x1, y=y1, width=x2-x1, height=y2-y1),
                        "x1": x1, "y1": y1, "x2": x2, "y2": y2
                    })

            # 3. Tracking
            if req.camera_id not in self.trackers:
                self.trackers[req.camera_id] = CentroidTracker(max_disappeared=5)
            
            tracker = self.trackers[req.camera_id]
            # Update tracker and get mapping of index to object ID
            mapping = tracker.update(rects)
            
            # Assign IDs back to detections
            for i, det in enumerate(raw_detections):
                assigned_id = mapping.get(i)
                
                detection = Detection(
                    **{"class": det["class"]},
                    confidence=det["confidence"],
                    bbox=det["bbox"],
                    track_id=assigned_id
                )

                if req.analyze_detailed:
                    crop = self._get_crop(frame, det["x1"], det["y1"], det["x2"], det["y2"])
                    self._enrich_detection(detection, det["class"], crop)

                detections.append(detection)

            # 4. Track latency
            total_duration = (time.perf_counter() - start_time) * 1000
            self.latencies.append(total_duration)
            if len(self.latencies) > settings.LATENCY_HISTORY_SIZE:
                self.latencies.pop(0)
            
            logger.info(f"Inference complete: {req.camera_id} | {len(detections)} objects | Total: {total_duration:.2f}ms")
            return DetectResponse(camera_id=req.camera_id, timestamp=req.timestamp, detections=detections)
            
        finally:
            await self.queue.get()

    def _get_crop(self, frame: np.ndarray, x1: float, y1: float, x2: float, y2: float) -> np.ndarray:
        h, w = frame.shape[:2]
        ix1, iy1, ix2, iy2 = int(max(0, x1)), int(max(0, y1)), int(min(w, x2)), int(min(h, y2))
        return frame[iy1:iy2, ix1:ix2]

    def _enrich_detection(self, detection: Detection, cls_name: str, crop: np.ndarray):
        if cls_name in VEHICLE_CLASSES:
            try:
                # Color Analysis
                detection.color = color_analyzer.get_dominant_color(crop)
                detection.vehicle_type = cls_name
                
                # Plate Reading (LPR)
                # We only try to read plates if the crop is large enough to likely contain one
                if crop.shape[0] > 50 and crop.shape[1] > 50:
                    detection.license_plate = plate_analyzer.read_plate(crop)
            except Exception as e:
                logger.error(f"Enrichment error for vehicle {cls_name}: {str(e)}")
            
        elif cls_name == "person":
            detection.attributes = {"clothing": "unknown", "action": "moving"}

    def get_p95_latency(self) -> float:
        if not self.latencies:
            return 0.0
        return float(np.percentile(self.latencies, 95))

# Global instance
yolo_service = YoloService()
