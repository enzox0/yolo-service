# YOLO11 Inference Microservice

A high-performance FastAPI service for real-time object detection and tracking using YOLO11. This service is designed to be called by the `footage-hub` backend to process surveillance frames.

## Features
- **YOLO11 Integration**: Uses the latest YOLO11n model for fast inference.
- **Object Tracking**: Implements ByteTrack for persistent object IDs across frames.
- **FastAPI**: Asynchronous API endpoints for low-latency communication.
- **Auto-Hardware Detection**: Automatically uses NVIDIA CUDA if available, otherwise falls back to CPU.

## Prerequisites
- **Python 3.11+**
- **uv** (recommended) or **pip**
- **FFmpeg** (required by OpenCV for some image operations)

## Setup & Installation

### Option 1: Using `uv` (Recommended)
[uv](https://github.com/astral-sh/uv) is a fast Python package manager.

1. Install dependencies:
   ```powershell
   uv sync
   ```

2. Run the service:
   ```powershell
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Option 2: Using standard `pip`
1. Create a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```powershell
   pip install -r pyproject.toml
   # Or manually:
   pip install fastapi "uvicorn[standard]" ultralytics torch pydantic python-multipart opencv-python numpy
   ```

3. Run the service:
   ```powershell
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Running with Docker
A Dockerfile is provided for containerized deployment, optimized for NVIDIA GPUs.

```bash
docker build -t yolo-service .
docker run -p 8000:8000 --gpus all yolo-service
```

## Backend Integration
To connect this service to the `footage-hub` backend:

1. Locate the `.env` file in the `backend/` directory.
2. Set the `YOLO_SERVICE_URL`:
   ```env
   YOLO_SERVICE_URL=http://localhost:8000
   ```
3. The backend's `YoloDetector` will now automatically route frames to this service.

## API Endpoints (v1)
All modern endpoints are prefixed with `/api/v1`.

- `GET /api/v1/health`: Returns detailed service status, hardware utilization, and P95 latency.
- `POST /api/v1/detect`: Accepts base64 encoded images for inference.

> **Note**: Legacy root endpoints `/health` and `/detect` are maintained for backward compatibility but will be deprecated in future versions.

## Project Structure
The service follows an enterprise-level layout:
- `app/api/`: API route definitions and versioning.
- `app/core/`: Global configuration, logging, and security.
- `app/models/`: Pydantic data models (schemas).
- `app/services/`: Core business logic and model management.
- `models/`: Directory for YOLO weight files (`.pt`).

## Testing the Service

### 1. Health Check
Verify the service is up by checking the health endpoint:
```powershell
# Using curl (Windows/Linux)
curl http://localhost:8000/health
```
Expected response: `{"status":"ok", "model":"yolo11n", "device":"cuda" or "cpu", ...}`

### 2. Manual Inference Test
Use the [test_service.py](test_service.py) script to verify that the model correctly detects objects in an image.

1. Ensure you have an image file ready (e.g., `test.jpg`).
2. Run the test script:
   ```powershell
   # If using uv
   uv run test_service.py --image path/to/your/image.jpg

   # If using standard python
   python test_service.py --image path/to/your/image.jpg
   ```
   The script will print the detected objects, their confidence scores, and their bounding boxes.

### 3. Integrated Test
Once the service is running and the backend `.env` is configured with `YOLO_SERVICE_URL=http://localhost:8000`, the backend logs should confirm initialization:
`YoloDetector initialized with service URL: http://localhost:8000`
