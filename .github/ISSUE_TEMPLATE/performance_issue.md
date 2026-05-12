---
name: Performance Issue
about: Report performance problems, slow inference, or resource usage issues
title: '[PERFORMANCE] '
labels: performance
assignees: ''
---

## Performance Issue Description
A clear description of the performance problem you're experiencing.

## Current Performance
**Metrics:**
- Average inference time: _____ ms
- P95 latency: _____ ms
- P99 latency: _____ ms
- Throughput: _____ requests/second
- Memory usage: _____ MB/GB
- GPU utilization: _____ %
- CPU utilization: _____ %

**How measured:**
- [ ] `/api/v1/health` endpoint metrics
- [ ] Custom benchmarking script
- [ ] Application logs
- [ ] System monitoring tools (specify: _____)

## Expected Performance
What performance level did you expect?
- Expected inference time: _____ ms
- Expected throughput: _____ requests/second
- Expected resource usage: _____

## Environment
**Hardware:**
- CPU: [e.g., Intel i7-12700K, AMD Ryzen 9 5900X]
- RAM: [e.g., 32GB DDR4]
- GPU: [e.g., NVIDIA RTX 3080, Tesla T4, None]
- Storage: [e.g., NVMe SSD, HDD]

**Software:**
- OS: [e.g., Windows 11, Ubuntu 22.04]
- Python Version: [e.g., 3.11.5]
- PyTorch Version: [e.g., 2.1.0]
- CUDA Version: [e.g., 12.1]
- Service Version: [e.g., v0.1.0]

**Model Configuration:**
- Model: [e.g., yolo11n.pt, yolo11m.pt]
- Model size: [e.g., 6.2MB, 49.7MB]
- Input image resolution: [e.g., 640x480, 1920x1080]
- Batch size: [e.g., 1, 4, 8]

## Workload Details
**Request Pattern:**
- Request rate: [e.g., 10 requests/second]
- Concurrent requests: [e.g., 1, 5, 10]
- Image size: [e.g., 1920x1080, 640x480]
- Image format: [e.g., JPEG, PNG]
- Average image file size: [e.g., 500KB]

**Usage Pattern:**
- [ ] Single image inference
- [ ] Batch processing
- [ ] Continuous video stream
- [ ] Burst traffic
- [ ] Other: _____

## Reproduction Steps
1. Start service with configuration: _____
2. Send requests using: _____
3. Measure performance with: _____
4. Observe: _____

## Benchmarking Script
If you have a script to reproduce the issue, share it here:

```python
# Example benchmarking code
import time
import requests

# Your benchmarking code here
```

## Profiling Data
If you've done any profiling, share the results:

```
# CPU profiling output
# Memory profiling output
# GPU profiling output
```

## Bottleneck Analysis
Have you identified where the bottleneck is?
- [ ] Image decoding
- [ ] Model inference
- [ ] Post-processing
- [ ] Network I/O
- [ ] Disk I/O
- [ ] Memory allocation
- [ ] Unknown

## Comparison
**Performance in other scenarios:**
- Performance with smaller images: _____
- Performance with different model: _____
- Performance on different hardware: _____
- Performance with official Ultralytics CLI: _____

## Logs
Relevant logs showing the performance issue:

```
Paste logs here
```

## Configuration
**Service Configuration:**
```yaml
# Relevant configuration settings
# .env or config file contents (remove sensitive data)
```

**Docker Configuration (if applicable):**
```yaml
# docker-compose.yml or Dockerfile settings
```

## Attempted Solutions
What have you tried to improve performance?
- [ ] Changed model size
- [ ] Adjusted image resolution
- [ ] Modified batch size
- [ ] Changed hardware
- [ ] Tuned configuration parameters
- [ ] Other: _____

Results of attempted solutions: _____

## Impact
How is this affecting your use case?
- [ ] Blocking production deployment
- [ ] Degraded user experience
- [ ] Increased infrastructure costs
- [ ] Unable to meet SLA requirements
- [ ] Other: _____

## Additional Context
- Are there specific times when performance degrades?
- Does performance degrade over time (memory leak)?
- Any error messages or warnings in logs?
- Network latency considerations?

## Possible Optimizations
If you have ideas for optimization, share them:
- Model quantization?
- Batch processing?
- Caching strategies?
- Hardware upgrades?

## Checklist
- [ ] I have measured actual performance metrics
- [ ] I have compared with expected performance
- [ ] I have provided detailed environment information
- [ ] I have tried basic troubleshooting steps
- [ ] I have checked for similar performance issues
