import cv2
from ultralytics import YOLO
import numpy as np
from config import YOLO_CONFIG

class EmergencyDetector:
    def __init__(self, model_path=None, vehicle_classes=None, emergency_classes=None,
                 conf_threshold=None, img_size=None, iou_threshold=None):
        # Initialize with config values or override with parameters
        self.model = YOLO(model_path or YOLO_CONFIG['model_path'])
        self.vehicle_classes = vehicle_classes or YOLO_CONFIG['vehicle_classes']
        self.emergency_classes = emergency_classes or YOLO_CONFIG['emergency_classes']
        self.conf_threshold = conf_threshold or YOLO_CONFIG['conf_threshold']
        self.img_size = img_size or YOLO_CONFIG['img_size']
        self.iou_threshold = iou_threshold or YOLO_CONFIG['iou_threshold']
        
    def detect(self, frame):
        """Process frame and return vehicle count, emergency status, and vehicle types"""
        # Maintain aspect ratio while resizing
        h, w = frame.shape[:2]
        scale = min(self.img_size / h, self.img_size / w)
        new_h, new_w = int(h * scale), int(w * scale)
        resized = cv2.resize(frame, (new_w, new_h))
        
        # Run detection with optimized parameters
        results = self.model(
            resized,
            imgsz=self.img_size,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            classes=self._get_class_ids(),
            device='cpu'
        )
        
        vehicle_count = 0
        emergency_detected = False
        vehicle_types = {}
        
        for box in results[0].boxes:
            class_id = int(box.cls)
            class_name = self.model.names[class_id]
            
            if class_name in self.vehicle_classes:
                vehicle_count += 1
                vehicle_types[class_name] = vehicle_types.get(class_name, 0) + 1
                
                if class_name in self.emergency_classes:
                    emergency_detected = True
        
        return vehicle_count, emergency_detected, vehicle_types
    
    def _get_class_ids(self):
        """Get YOLO class IDs for our target classes"""
        return [
            idx for idx, name in self.model.names.items() 
            if name in self.vehicle_classes + self.emergency_classes
        ]