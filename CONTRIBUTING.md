# Contributing to YOLO11 Inference Microservice

Thank you for your interest in contributing to the YOLO11 Inference Microservice! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors. We expect:
- Respectful communication
- Constructive feedback
- Focus on what is best for the community
- Empathy towards other contributors

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```powershell
   git clone https://github.com/your-username/yolo-service.git
   cd yolo-service
   ```
3. **Add the upstream repository**:
   ```powershell
   git remote add upstream https://github.com/original-owner/yolo-service.git
   ```

## Development Setup

### Prerequisites
- Python 3.11 or higher
- uv (recommended) or pip
- FFmpeg
- Git

### Setting Up Your Development Environment

1. **Install dependencies using uv** (recommended):
   ```powershell
   uv sync
   ```

   Or using pip:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e .
   ```

2. **Verify the installation**:
   ```powershell
   uv run uvicorn app.main:app --reload
   ```

3. **Test the service**:
   ```powershell
   curl http://localhost:8000/api/v1/health
   ```

## How to Contribute

### Reporting Bugs

Before creating a bug report:
- Check the existing issues to avoid duplicates
- Collect relevant information (OS, Python version, error messages)

When creating a bug report, include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots or logs if applicable
- Environment details (OS, Python version, GPU/CPU)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- A clear description of the proposed feature
- Use cases and benefits
- Potential implementation approach
- Any relevant examples or references

### Code Contributions

1. **Create a new branch** for your feature or fix:
   ```powershell
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. **Make your changes** following the coding standards

3. **Test your changes** thoroughly

4. **Commit your changes** with clear commit messages

5. **Push to your fork**:
   ```powershell
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Code Organization
```python
# Standard library imports
import os
from typing import List, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
import numpy as np

# Local imports
from app.core.config import settings
from app.models.schemas import DetectionResponse
```

### Documentation
- Add docstrings to all public functions, classes, and modules
- Use Google-style docstrings:
  ```python
  def detect_objects(image: np.ndarray, confidence: float = 0.5) -> List[Detection]:
      """
      Detect objects in an image using YOLO11.
      
      Args:
          image: Input image as numpy array
          confidence: Minimum confidence threshold (0.0 to 1.0)
          
      Returns:
          List of Detection objects containing bounding boxes and labels
          
      Raises:
          ValueError: If image is invalid or confidence is out of range
      """
      pass
  ```

### Error Handling
- Use appropriate exception types
- Provide meaningful error messages
- Log errors with appropriate severity levels
- Handle edge cases gracefully

## Testing Guidelines

### Running Tests
```powershell
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html
```

### Writing Tests
- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

Example:
```python
def test_detect_endpoint_returns_valid_response():
    # Arrange
    client = TestClient(app)
    test_image = encode_test_image("test.jpg")
    
    # Act
    response = client.post("/api/v1/detect", json={"image": test_image})
    
    # Assert
    assert response.status_code == 200
    assert "detections" in response.json()
```

## Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(api): add batch detection endpoint

Implement new endpoint for processing multiple images in a single request.
This improves throughput for bulk processing scenarios.

Closes #123
```

```
fix(yolo): resolve memory leak in model inference

Fixed issue where CUDA tensors were not being properly released after inference,
causing memory accumulation over time.

Fixes #456
```

## Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add tests** for new features or bug fixes
3. **Ensure all tests pass** before submitting
4. **Update the README.md** if needed
5. **Fill out the PR template** completely
6. **Link related issues** using keywords (Fixes #123, Closes #456)

### PR Title Format
Use the same format as commit messages:
```
feat(api): add support for video stream processing
```

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No new warnings generated
```

### Review Process
- At least one maintainer review is required
- Address all review comments
- Keep the PR focused on a single concern
- Be responsive to feedback

## Development Tips

### Running in Development Mode
```powershell
# With auto-reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# With debug logging
uv run uvicorn app.main:app --reload --log-level debug
```

### Testing with Different Models
Place YOLO model files in the `models/` directory and update the configuration:
```python
# app/core/config.py
MODEL_PATH = "models/yolo11n.pt"  # Change to your model
```

### Performance Profiling
```python
# Add timing decorators for performance analysis
import time
from functools import wraps

def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper
```

## Questions or Need Help?

- Open an issue with the `question` label
- Check existing documentation and issues first
- Provide context and details in your questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE.md).

---

Thank you for contributing to the YOLO11 Inference Microservice! 🚀
