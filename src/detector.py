from ultralytics import YOLO
import config

class ObjectDetector:
    def __init__(self, model_path=config.MODEL_PATH):
        self.model = YOLO(model_path)
    
    def detect(self, frame):
        """
        Detects objects in the frame.
        Returns a list of dictionaries in the enhanced schema:
        {
          "label": "<string>",
          "confidence": <float>,
          "distance": "near | medium | far",
          "position": "left | center | right",
          "is_dangerous": <boolean>
          "box": [x1, y1, x2, y2] (kept for visualization)
        }
        """
        height, width, _ = frame.shape
        frame_area = width * height
        
        # stream=True for efficiency
        results = self.model.predict(frame, conf=config.CONFIDENCE_THRESHOLD, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Metadata Extraction
                # 1. Label & Conf
                cls = int(box.cls[0].item())
                label = self.model.names[cls]
                conf = box.conf[0].item()
                
                # 2. Position (Center of box relative to frame width)
                cx = (x1 + x2) / 2
                if cx < width * 0.33:
                    position = "left"
                elif cx > width * 0.66:
                    position = "right"
                else:
                    position = "center"
                
                # 3. Distance (Based on Area coverage)
                obj_area = (x2 - x1) * (y2 - y1)
                ratio = obj_area / frame_area
                
                if ratio >= config.AREA_NEAR:
                    distance = "near"
                elif ratio >= config.AREA_MEDIUM:
                    distance = "medium"
                else:
                    distance = "far"
                
                # 4. Safety
                is_dangerous = label.lower() in config.DANGEROUS_OBJECTS
                
                detections.append({
                    'label': label,
                    'confidence': conf,
                    'distance': distance,
                    'position': position,
                    'is_dangerous': is_dangerous,
                    'box': [x1, y1, x2, y2]
                })
        return detections
