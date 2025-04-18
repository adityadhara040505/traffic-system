import time
import cv2
from threading import Thread, Lock
from collections import defaultdict
from config import TIMING, YOLO_CONFIG, CAMERA_CONFIG
from utils.gpio_controller import GPIOManager
from utils.emergency_detector import EmergencyDetector

class TrafficSystem:
    def __init__(self):
        self.gpio = GPIOManager()
        self.detector = EmergencyDetector()
        self.timing = TIMING
        self.camera_config = CAMERA_CONFIG
        
        self.vehicle_counts = defaultdict(int)
        self.vehicle_types = defaultdict(dict)
        self.emergency_flag = False
        self.lock = Lock()
        self.frame_count = 0
        
        # Clockwise direction cycle
        self.direction_cycle = ['north', 'east', 'south', 'west']
        self.current_direction = self.direction_cycle[0]

    def _init_camera(self, source):
        """Initialize camera with optimized settings"""
        cap = cv2.VideoCapture(source)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_config['resolution'][0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_config['resolution'][1])
        cap.set(cv2.CAP_PROP_FPS, 15)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        return cap

    def _set_phase(self, green_direction):
        """Set lights for current phase"""
        self.gpio.reset_all_lights()
        
        # Set green for current direction
        self.gpio.set_light(green_direction, 'green', True)
        
        # Set red for all other directions
        for direction in self.direction_cycle:
            if direction != green_direction:
                self.gpio.set_light(direction, 'red', True)

    def _yellow_transition(self, direction):
        """Yellow light transition"""
        self.gpio.set_light(direction, 'green', False)
        self.gpio.set_light(direction, 'yellow', True)

    def _calculate_green_time(self, direction):
        """Calculate green time based on vehicle count and types"""
        count = self.vehicle_counts.get(direction, 0)
        types = self.vehicle_types.get(direction, {})
        
        # Weight different vehicle types
        vehicle_weight = {
            'car': 1,
            'motorcycle': 0.7,
            'truck': 2.5,
            'bus': 3,
            'van': 1.8,
            'trailer': 2.8
        }
        
        weighted_count = sum(
            vehicle_weight.get(veh_type, 1) * cnt 
            for veh_type, cnt in types.items()
        )
        
        # Normalize and calculate time
        max_weighted = 50  # Adjust based on your intersection capacity
        ratio = min(weighted_count / max_weighted, 1.0)
        
        return int(
            self.timing['min_green_time'] + 
            ratio * (self.timing['max_green_time'] - self.timing['min_green_time'])
        )

    def _get_opposite_direction(self, direction):
        """Get the opposite direction"""
        opposites = {'north': 'south', 'south': 'north', 
                    'east': 'west', 'west': 'east'}
        return opposites[direction]

    def normal_cycle(self):
        """Dynamic traffic light cycle based on vehicle counts"""
        while True:
            if self.emergency_flag:
                time.sleep(1)
                continue
                
            current = self.current_direction
            opposite = self._get_opposite_direction(current)
            
            # Calculate green time based on vehicle count
            green_time = self._calculate_green_time(current)
            
            # Current direction green, opposite red
            self._set_phase(current)
            time.sleep(green_time)
            
            # Current direction yellow
            self._yellow_transition(current)
            time.sleep(self.timing['yellow_time'])
            
            # All red
            self.gpio.reset_all_lights()
            self.gpio.set_all_lights('red', True)
            time.sleep(self.timing['all_red_time'])
            
            # Move to next direction in cycle
            current_index = self.direction_cycle.index(self.current_direction)
            self.current_direction = self.direction_cycle[(current_index + 1) % 4]

    def run_detection(self):
        """Vehicle detection from all cameras"""
        caps = {
            direction: self._init_camera(config['source'])
            for direction, config in self.camera_config.items()
            if direction in self.direction_cycle
        }
        
        try:
            while True:
                for direction, cap in caps.items():
                    ret, frame = cap.read()
                    if not ret:
                        continue
                        
                    if self.frame_count % self.camera_config['frame_skip'] == 0:
                        vehicle_count, emergency, vehicle_types = self.detector.detect(frame)
                        
                        with self.lock:
                            self.vehicle_counts[direction] = vehicle_count
                            self.vehicle_types[direction] = vehicle_types
                            
                            if emergency and not self.emergency_flag:
                                self.emergency_flag = True
                                self.gpio.emergency_blink(self.timing['emergency_blink_duration'])
                                self.emergency_flag = False
                    
                    self.frame_count += 1
        finally:
            for cap in caps.values():
                cap.release()

    def trigger_emergency(self):
        """Handle emergency vehicle detection"""
        self.emergency_flag = True
        self.gpio.emergency_blink(self.timing['emergency_blink_duration'])
        self.emergency_flag = False

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