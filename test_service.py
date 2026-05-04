import base64
import requests
import argparse
import sys
import os
import cv2
import numpy as np
from datetime import datetime

def test_inference(file_path, service_url="http://localhost:8000"):
    """
    Tests the YOLO service by sending an image or video for detection.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    ext = os.path.splitext(file_path)[1].lower()
    is_video = ext in ['.mp4', '.mov', '.avi', '.mkv']
    is_image = ext in ['.jpg', '.jpeg', '.png', '.webp']

    if not is_image and not is_video:
        print(f"Error: Unsupported file extension {ext}")
        return

    try:
        if is_image:
            print(f"Processing image: {file_path}")
            with open(file_path, "rb") as image_file:
                img_bytes = image_file.read()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            send_request(img_base64, "image", service_url)
        
        elif is_video:
            print(f"Processing video: {file_path}")
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                print(f"Error: Could not open video file {file_path}")
                return
            
            # Extract the first frame for testing (or you could loop through)
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                print("Error: Could not read frame from video")
                return
                
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            send_request(img_base64, "video_frame", service_url)

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def send_request(img_base64, source_type, service_url):
    try:
        # 2. Prepare payload
        payload = {
            "camera_id": "test_cli_client",
            "timestamp": datetime.now().isoformat(),
            "image_base64": img_base64,
            "analyze_detailed": True,
            "source_type": "video" if source_type == "video_frame" else "image"
        }

        # 3. Send POST request to /api/v1/detect
        url = f"{service_url.rstrip('/')}/api/v1/detect"
        print(f"Sending {source_type} request to {url}...")
        
        start_time = datetime.now()
        response = requests.post(url, json=payload, timeout=30)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds() * 1000

        if response.status_code == 200:
            data = response.json()
            detections = data.get("detections", [])
            print(f"\n✅ Success! (Response time: {duration:.2f}ms)")
            print(f"Found {len(detections)} objects:")
            
            if not detections:
                print("  (No objects detected)")
            
            for i, d in enumerate(detections, 1):
                cls = d.get('class', 'unknown')
                conf = d.get('confidence', 0)
                track_id = d.get('track_id')
                bbox = d.get('bbox', {})
                color = d.get('color')
                plate = d.get('license_plate')
                
                track_str = f" [ID: {track_id}]" if track_id is not None else ""
                attr_str = []
                if color: attr_str.append(f"Color: {color}")
                if plate: attr_str.append(f"Plate: {plate}")
                attrs = f" ({', '.join(attr_str)})" if attr_str else ""
                
                print(f"  {i}. {cls}{track_str}{attrs}: {conf:.2%} confidence")
                print(f"     BBox: x={bbox.get('x'):.1f}, y={bbox.get('y'):.1f}, w={bbox.get('width'):.1f}, h={bbox.get('height'):.1f}")
        else:
            print(f"❌ Error: Received status code {response.status_code}")
            try:
                print(response.json())
            except:
                print(response.text)

    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to service at {service_url}. Ensure the service is running.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test YOLO Service Inference")
    parser.add_argument("--image", required=True, help="Path to an image or video file")
    parser.add_argument("--url", default="http://localhost:8000", help="Service URL (default: http://localhost:8000)")
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    test_inference(args.image, args.url)
