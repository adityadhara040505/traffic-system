from gpiozero import LEDBoard, Device
from gpiozero.pins.mock import MockFactory
import platform
from config import GPIO_CONFIG

class GPIOManager:
    """Cross-platform GPIO manager (real on Pi, mock on Windows/Mac)"""
    def __init__(self):
        # Use mock pins on non-Linux systems
        if platform.system() != 'Linux':
            Device.pin_factory = MockFactory()
        
        # Initialize LED boards
        self.lights = {
            direction: LEDBoard(
                red=config['red'],
                yellow=config['yellow'],
                green=config['green']
            )
            for direction, config in GPIO_CONFIG.items()
        }

    def set_light(self, direction, color, state):
        """Control a single light (e.g., 'north', 'red', True)"""
        light = getattr(self.lights[direction], color)
        light.on() if state else light.off()

    def set_all_lights(self, color, state):
        """Set all lights of one color (e.g., all red ON)"""
        for direction in self.lights.values():
            getattr(direction, color).on() if state else getattr(direction, color).off()

    def reset_all_lights(self):
        """Turn off all traffic lights"""
        for light in self.lights.values():
            light.off()

    def emergency_blink(self, duration):
        """Blink all red lights for emergency"""
        from time import sleep
        for _ in range(int(duration * 2)):  # 2 blinks/second
            self.set_all_lights('red', True)
            sleep(0.25)
            self.set_all_lights('red', False)
            sleep(0.25)