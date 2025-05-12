GPIO_CONFIG = {
    'north': {
        'red': 17,     # Physical Pin 11 (GPIO 17)
        'yellow': 27,   # Physical Pin 13 (GPIO 27)
        'green': 22     # Physical Pin 15 (GPIO 22)
    },
    'east': {
        'red': 19,     # Physical Pin 35 (GPIO 19)
        'yellow': 26,   # Physical Pin 37 (GPIO 26)
        'green': 21     # Physical Pin 40 (GPIO 21)
    },
    'south': {
        'red': 5,       # Physical Pin 29 (GPIO 5)
        'yellow': 6,    # Physical Pin 31 (GPIO 6)
        'green': 13      # Physical Pin 33 (GPIO 13)
    },
    'west': {
        'red': 20,      # Physical Pin 38 (GPIO 20)
        'yellow': 16,    # Physical Pin 36 (GPIO 16)
        'green': 12      # Physical Pin 32 (GPIO 12)
    }
}

PIN_NUMBERING = 'BCM'

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
    'north': {'source': 'http://192.168.32.56:4747/video'},
    'east': {'source': 'http://192.168.32.252:4747/video'},
    'south': {'source': 'http://192.168.32.83:4747/video'},
    'west': {'source': 'http://192.168.32.23:4747/video'},
    'frame_skip': 20,
    'resolution': (640, 480)
}
