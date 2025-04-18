GPIO_CONFIG = {
    'north': {'red': 17, 'yellow': 27, 'green': 22},
    'east': {'red': 5, 'yellow': 6, 'green': 13},
    'south': {'red': 26, 'yellow': 16, 'green': 20},
    'west': {'red': 12, 'yellow': 25, 'green': 8}
}

TIMING = {
    'min_green_time': 15,       # Minimum green time (seconds)
    'max_green_time': 120,      # Maximum green time (seconds)
    'yellow_time': 3,
    'all_red_time': 2,
    'emergency_blink_duration': 10,
    'vehicle_count_interval': 5  # How often to count vehicles (seconds)
}

YOLO_CONFIG = {
    'model_path': 'assets/yolov8n.pt',
    'vehicle_classes': ['car', 'truck', 'bus', 'motorcycle', 'van', 'trailer'],
    'emergency_classes': ['ambulance', 'fire truck', 'police car'],
    'conf_threshold': 0.65,
    'img_size': 416,
    'iou_threshold': 0.45
}

CAMERA_CONFIG = {
    'north': {'source': 'http://192.168.28.170:4747/video'},
    'east': {'source': 'http://192.168.28.170:4747/video'},
    'south': {'source': 'http://192.168.28.170:4747/video'},
    'west': {'source': 'http://192.168.28.170:4747/video'},
    'frame_skip': 20,
    'resolution': (640, 480)
}