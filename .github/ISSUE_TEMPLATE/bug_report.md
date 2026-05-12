---
name: Bug Report
about: Report a bug or unexpected behavior in the YOLO service
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
A clear and concise description of what the bug is.

## To Reproduce
Steps to reproduce the behavior:
1. Start the service with '...'
2. Send request to '...'
3. With payload '...'
4. See error

## Expected Behavior
A clear and concise description of what you expected to happen.

## Actual Behavior
What actually happened instead.

## Error Messages
```
Paste any error messages, stack traces, or logs here
```

## Environment
**Operating System:**
- [ ] Windows
- [ ] Linux
- [ ] macOS
- [ ] Docker

**Python Version:**
- Version: [e.g., 3.11.5]

**Package Manager:**
- [ ] uv
- [ ] pip
- [ ] conda

**Hardware:**
- [ ] CPU only
- [ ] NVIDIA GPU (specify model: _______)
- [ ] AMD GPU
- [ ] Apple Silicon

**CUDA Version (if applicable):**
- Version: [e.g., 12.1]

**Service Version:**
- Version/Commit: [e.g., v0.1.0 or commit hash]

## Installation Method
- [ ] Installed via `uv sync`
- [ ] Installed via `pip install`
- [ ] Running in Docker container
- [ ] Other: _____

## Configuration
**Model Used:**
- [ ] yolo11n.pt (default)
- [ ] yolo11s.pt
- [ ] yolo11m.pt
- [ ] yolo11l.pt
- [ ] yolo11x.pt
- [ ] Custom model: _____

**Service Configuration:**
```yaml
# Paste relevant configuration from .env or config files
# Remove any sensitive information like API keys
```

## Request Details (if applicable)
**Endpoint:**
- [ ] `/api/v1/health`
- [ ] `/api/v1/detect`
- [ ] Legacy endpoint
- [ ] Other: _____

**Request Payload:**
```json
{
  "image": "base64_string_truncated...",
  "confidence": 0.5
}
```

**Response Received:**
```json
{
  "error": "..."
}
```

## Screenshots
If applicable, add screenshots to help explain your problem.

## Additional Context
Add any other context about the problem here. For example:
- Does this happen consistently or intermittently?
- Did this work in a previous version?
- Are there any workarounds you've found?
- Network configuration or firewall settings
- Resource constraints (memory, disk space)

## Possible Solution
If you have ideas on how to fix this, please share them here.

## Checklist
- [ ] I have searched existing issues to avoid duplicates
- [ ] I have included all relevant information above
- [ ] I have removed any sensitive information (API keys, credentials)
- [ ] I can reproduce this issue consistently
- [ ] I have tested with the latest version
