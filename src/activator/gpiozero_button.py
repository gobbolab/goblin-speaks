from .base import Activator
from src.config import Config
from gpiozero import Button


class GpioZeroButton(Activator):
    """
    A GPIO button/sensor activator backed by gpiozero's Button class.
    Compatible with any component that signals via a digital GPIO pin:
    physical buttons, IR beam sensors, reed switches, etc.
    """
    def __init__(self, config_prefix=None):
        config = Config()
        prefix = config_prefix or 'activator.gpiozero_button'
        print("Values Loaded:")
        self.trigger_pin = config.get(f'{prefix}.trigger_pin', 21)
        print(f"Trigger Pin: {self.trigger_pin}")
        self.sensor = Button(self.trigger_pin, pull_up=True)

    def start(self, callback):
        print(f"Initializing GpioZeroButton activator on pin {self.trigger_pin}...")
        # Depending on wiring, may need `when_released = callback` if it triggers when the signal is restored.
        self.sensor.when_pressed = callback
        print("GpioZeroButton Activator is ready. Waiting for trigger...")

    def shutdown(self):
        self.sensor.close()
        del self.sensor
        print("GpioZeroButton Activator is shut down.")
