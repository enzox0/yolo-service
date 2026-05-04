from pydantic import BaseModel, Field

class BBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

class Detection(BaseModel):
    class_name: str = Field(alias="class")
    confidence: float
    bbox: BBox
    track_id: int | None = None
    color: str | None = None
    license_plate: str | None = None
    vehicle_type: str | None = None
    attributes: dict | None = None

class DetectRequest(BaseModel):
    camera_id: str
    timestamp: str
    image_base64: str
    analyze_detailed: bool = False
    roi: BBox | None = None
    source_type: str | None = "image" # "image" or "video"

class DetectResponse(BaseModel):
    camera_id: str
    timestamp: str
    detections: list[Detection]

class HealthResponse(BaseModel):
    status: str
    model: str
    device: str
    queue_depth: int
    p95_latency_ms: float | None = None
