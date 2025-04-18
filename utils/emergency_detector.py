import cv2
from ultralytics import YOLO

class EmergencyDetector:
    """Detects emergency vehicles using YOLO"""
    def __init__(self, model_path, classes, conf_threshold=0.5, img_size=320):
        self.model = YOLO(model_path)
        self.classes = classes
        self.conf_threshold = conf_threshold
        self.img_size = img_size

    def detect(self, frame):
        """Process a frame and return True if emergency vehicle detected"""
        frame = cv2.resize(frame, (self.img_size, self.img_size))
        results = self.model(frame, imgsz=self.img_size, conf=self.conf_threshold, device='cpu')
        
        for box in results[0].boxes:
            if self.model.names[int(box.cls)] in self.classes:
                return True
        return False