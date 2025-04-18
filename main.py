import time
import cv2
from threading import Thread
from config import TIMING, YOLO_CONFIG, CAMERA_CONFIG
from utils.gpio_controller import GPIOManager
from utils.emergency_detector import EmergencyDetector

class TrafficSystem:
    def __init__(self):
        self.gpio = GPIOManager()
        self.detector = EmergencyDetector(
            model_path=YOLO_CONFIG['model_path'],
            classes=YOLO_CONFIG['emergency_classes'],
            conf_threshold=YOLO_CONFIG['conf_threshold'],
            img_size=YOLO_CONFIG['img_size']
        )
        self.timing = TIMING
        self.camera_config = CAMERA_CONFIG

    def _set_phase(self, green_directions, red_directions):
        """Set lights for a traffic phase"""
        self.gpio.reset_all_lights()
        for direction in green_directions:
            self.gpio.set_light(direction, 'green', True)
        for direction in red_directions:
            self.gpio.set_light(direction, 'red', True)

    def _yellow_transition(self, directions):
        """Yellow light transition"""
        for direction in directions:
            self.gpio.set_light(direction, 'green', False)
            self.gpio.set_light(direction, 'yellow', True)

    def normal_cycle(self):
        """Standard traffic light cycle"""
        while True:
            # North-South Green, East-West Red
            self._set_phase(['north', 'south'], ['east', 'west'])
            time.sleep(self.timing['green_time'])

            # North-South Yellow
            self._yellow_transition(['north', 'south'])
            time.sleep(self.timing['yellow_time'])

            # All Red
            self.gpio.reset_all_lights()
            self.gpio.set_all_lights('red', True)
            time.sleep(self.timing['all_red_time'])

            # East-West Green, North-South Red
            self._set_phase(['east', 'west'], ['north', 'south'])
            time.sleep(self.timing['green_time'])

            # East-West Yellow
            self._yellow_transition(['east', 'west'])
            time.sleep(self.timing['yellow_time'])

            # All Red
            self.gpio.reset_all_lights()
            self.gpio.set_all_lights('red', True)
            time.sleep(self.timing['all_red_time'])

    def run_detection(self):
        """Emergency vehicle detection"""
        cap = cv2.VideoCapture(self.camera_config['source'])
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % self.camera_config['frame_skip'] == 0:
                if self.detector.detect(frame):
                    self.gpio.emergency_blink(self.timing['emergency_blink_duration'])

    def run(self):
        """Start the system"""
        try:
            Thread(target=self.normal_cycle, daemon=True).start()
            Thread(target=self.run_detection, daemon=True).start()
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.gpio.reset_all_lights()
            print("\nSystem stopped safely")

if __name__ == "__main__":
    system = TrafficSystem()
    system.run()