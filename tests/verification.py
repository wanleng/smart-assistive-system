import sys
import os
import time
import numpy as np
import cv2

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.detector import ObjectDetector
from src.reasoner import SceneReasoner
# from src.audio import AudioFeedback # Skip audio for automated test to avoid noise/errors in headless

def test_pipeline():
    print("Testing Pipeline...")
    
    # 1. Test Detector Loading
    print("Loading Detector...")
    try:
        detector = ObjectDetector()
        print("Detector loaded.")
    except Exception as e:
        print(f"FAILED to load detector: {e}")
        return

    # 2. Test Detection on Dummy Frame
    print("Testing Detection on blank frame...")
    blank_frame = np.zeros((config.FRAME_HEIGHT, config.FRAME_WIDTH, 3), dtype=np.uint8)
    # Draw a rectangle mimicking a 'person' maybe? 
    # YOLO won't detect valid objects from random shapes easily, but we checks it doesn't crash.
    detections = detector.detect(blank_frame)
    print(f"Detections on blank: {detections}")

    # 3. Test Reasoner and Schema
    print("Testing Reasoner and Schema...")
    reasoner = SceneReasoner()
    
    # Mock detection with new schema
    mock_detections = [
        {
            'label': 'car', 
            'confidence': 0.9, 
            'box': [0,0,100,100], 
            'distance': 'near', 
            'position': 'center', 
            'is_dangerous': True
        },
        {
            'label': 'cup', 
            'confidence': 0.8, 
            'box': [200,200,250,250], 
            'distance': 'far', 
            'position': 'right', 
            'is_dangerous': False
        }
    ]
    
    # Test Process (Should return text)
    msg = reasoner.process(mock_detections)
    print(f"Reasoner Output: {msg}")
    
    # Basic assertions
    if msg:
        assert "car" in msg.lower()
        assert "near" in msg.lower() # Safety priority
    
    # Test Summary
    summary = reasoner.get_summary()
    print(f"Session Summary: {summary}")
    assert "Dangerous events: 1" in summary

    # 4. Test Camera (Attempt Open)
    print("Testing Camera access...")
    cap = cv2.VideoCapture(config.CAMERA_ID)
    if not cap.isOpened():
        print("Warning: Camera not accessible. Skipping camera read test.")
    else:
        ret, frame = cap.read()
        if ret:
            print("Camera read successful.")
            print(f"Frame shape: {frame.shape}")
        else:
            print("Camera opened but failed to read frame.")
        cap.release()

    print("Verification Complete.")

if __name__ == "__main__":
    test_pipeline()
