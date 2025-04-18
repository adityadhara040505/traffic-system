from gpiozero import LEDBoard, Device
from gpiozero.pins.mock import MockFactory
import platform
from config import GPIO_CONFIG
import time

class GPIOManager:
    def __init__(self):
        # Use mock pins on non-Linux systems
        if platform.system() != 'Linux':
            Device.pin_factory = MockFactory()
        
        # Initialize LED boards
        self.lights = {
            direction: LEDBoard(
                red=config['red'],
                yellow=config['yellow'],
                green=config['green'],
                pwm=True  # Enable PWM for smooth transitions if needed
            )
            for direction, config in GPIO_CONFIG.items()
        }

    def set_light(self, direction, color, state):
        """Control a single light"""
        light = getattr(self.lights[direction], color)
        light.on() if state else light.off()

    def set_all_lights(self, color, state):
        """Set all lights of one color"""
        for direction in self.lights.values():
            getattr(direction, color).on() if state else getattr(direction, color).off()

    def reset_all_lights(self):
        """Turn off all traffic lights"""
        for light in self.lights.values():
            light.off()

    def emergency_blink(self, duration):
        """Blink all red lights for emergency"""
        end_time = time.time() + duration
        while time.time() < end_time:
            self.set_all_lights('red', True)
            time.sleep(0.25)
            self.set_all_lights('red', False)
            time.sleep(0.25)
        self.reset_all_lights()