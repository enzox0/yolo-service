# YOLO11 Inference Microservice

A high-performance FastAPI service for real-time object detection and tracking using YOLO11. This service provides REST API endpoints for processing images and video frames with advanced object detection capabilities.

## Features
- **YOLO11 Integration**: Uses the latest YOLO11n model for fast inference.
- **Object Tracking**: Implements ByteTrack for persistent object IDs across frames.
- **FastAPI**: Asynchronous API endpoints for low-latency communication.
- **Auto-Hardware Detection**: Automatically uses NVIDIA CUDA if available, otherwise falls back to CPU.
- **License Plate Recognition**: OCR-based plate detection and text extraction.
- **Vehicle Color Analysis**: Dominant color detection for tracked vehicles.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Running with Docker](#running-with-docker)
- [Backend Integration](#backend-integration)
- [API Endpoints](#api-endpoints-v1)
- [Project Structure](#project-structure)
- [Testing the Service](#testing-the-service)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Security](#security)

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

## Integration with Your Application
To integrate this service with your application:

1. Configure your application to point to the service URL:
   ```env
   YOLO_SERVICE_URL=http://localhost:8000
   ```
2. Make HTTP requests to the API endpoints (see [API Endpoints](#api-endpoints-v1) section)
3. The service accepts base64-encoded images and returns detection results in JSON format

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

### 3. Integration Test
Once the service is running, you can integrate it with your application by configuring the service URL and making API requests to the detection endpoints.

## Documentation

Comprehensive documentation is available in the following files:

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing to the project
  - Development setup and workflow
  - Coding standards and best practices
  - Testing guidelines
  - Pull request process

- **[LICENSE.md](LICENSE.md)** - Licensing information
  - MIT License for the project
  - Third-party library licenses
  - YOLO model licensing requirements
  - Commercial use considerations

- **[SECURITY.md](SECURITY.md)** - Security policy and best practices
  - Vulnerability reporting process
  - Security best practices for deployment
  - Production security checklist
  - Compliance considerations (GDPR, CCPA)

- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community guidelines and expectations

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

Key points:
- Follow PEP 8 style guidelines
- Add tests for new features
- Use conventional commit messages
- Ensure all tests pass before submitting

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

**Important**: The YOLO11 model weights are subject to the [Ultralytics AGPL-3.0 license](https://github.com/ultralytics/ultralytics/blob/main/LICENSE). Commercial use requires a commercial license from Ultralytics.

## Security

Security is a top priority. Please review our [Security Policy](SECURITY.md) for:
- Reporting vulnerabilities
- Security best practices
- Production deployment guidelines

**Never commit sensitive information** like API keys or credentials to the repository.

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](../../issues)
- **Discussions**: Ask questions in [GitHub Discussions](../../discussions)
- **Documentation**: Check the docs folder for detailed guides

## Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLO11
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [ByteTrack](https://github.com/ifzhang/ByteTrack) for object tracking
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) for license plate recognition

---

**Version**: 0.1.0  
**Last Updated**: May 12, 2026
