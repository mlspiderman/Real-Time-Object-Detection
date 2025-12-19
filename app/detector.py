from ultralytics import YOLO
import numpy as np

class ObjectDetector:
    def __init__(self, model_path="models/yolov8n.pt"):
        self.model = YOLO(model_path)
        
    def predict(self, frame: np.ndarray):
        results = self.model(frame)[0]
        
        detections = []
        for box in results.boxes:
            bbox = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            detections.append({
                "bbox": bbox,
                "confidence": conf,
                "class_id": cls,
                "class_name": results.names[cls]
            })
            
            return detections
