from gpiozero import LEDBoard, Device
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.rpigpio import RPiGPIOFactory
import platform
from config import GPIO_CONFIG, PIN_NUMBERING
import time

class GPIOManager:
    def __init__(self):
        # Initialize the appropriate pin factory
        if platform.system() == 'Linux':
            # For Raspberry Pi hardware
            if PIN_NUMBERING == 'BOARD':
                Device.pin_factory = RPiGPIOFactory()
                Device.pin_factory.pin_class.board_pin = True  # BOARD numbering
            else:
                Device.pin_factory = RPiGPIOFactory()  # Default BCM numbering
            pwm_enabled = True
        else:
            # For non-Linux systems (development)
            Device.pin_factory = MockFactory()
            pwm_enabled = False
            print("Running in mock mode - GPIO operations simulated")

        # Initialize LED boards
        self.lights = {
            direction: LEDBoard(
                red=config['red'],
                yellow=config['yellow'],
                green=config['green'],
                pwm=pwm_enabled,
                active_high=True,
                initial_value=False,
                pin_factory=Device.pin_factory
            )
            for direction, config in GPIO_CONFIG.items()
        }

        # Test all lights on startup
        self.test_lights()

    def test_lights(self):
        """Test all lights during initialization"""
        print("Testing all lights...")
        for color in ['red', 'yellow', 'green']:
            self.set_all_lights(color, True)
            time.sleep(0.5)
            self.set_all_lights(color, False)
        print("Light test complete")

    def set_light(self, direction, color, state):
        """Control a single light"""
        try:
            light = getattr(self.lights[direction], color)
            light.on() if state else light.off()
        except KeyError:
            print(f"Error: Invalid direction '{direction}'")
        except AttributeError:
            print(f"Error: Invalid color '{color}' for direction '{direction}'")

    def set_all_lights(self, color, state):
        """Set all lights of one color"""
        for direction in self.lights.values():
            try:
                getattr(direction, color).on() if state else getattr(direction, color).off()
            except AttributeError:
                print(f"Error: Invalid color '{color}'")

    def reset_all_lights(self):
        """Turn off all traffic lights"""
        for light in self.lights.values():
            light.off()

    def emergency_blink(self, duration):
        """Blink all red lights for emergency"""
        print(f"EMERGENCY: Blinking lights for {duration} seconds")
        end_time = time.time() + duration
        while time.time() < end_time:
            self.set_all_lights('red', True)
            time.sleep(0.25)
            self.set_all_lights('red', False)
            time.sleep(0.25)
        self.reset_all_lights()
        print("Emergency mode ended")

    def cleanup(self):
        """Clean up GPIO resources"""
        self.reset_all_lights()
        if platform.system() == 'Linux':
            Device.pin_factory.close()
        print("GPIO cleanup complete")
