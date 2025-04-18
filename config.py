GPIO_CONFIG = {
    'north': {'red': 17, 'yellow': 27, 'green': 22},
    'east': {'red': 5, 'yellow': 6, 'green': 13},
    'south': {'red': 26, 'yellow': 16, 'green': 20},
    'west': {'red': 12, 'yellow': 25, 'green': 8}
}

TIMING = {
    'green_time': 15,
    'yellow_time': 3,
    'all_red_time': 2,
    'emergency_blink_duration': 10
}

YOLO_CONFIG = {
    'model_path': 'assets/yolov8n.pt',
    'emergency_classes': ['ambulance', 'firetruck', 'police'],
    'conf_threshold': 0.5,
    'img_size': 320
}

CAMERA_CONFIG = {
    'source': 0,
    'frame_skip': 5
}