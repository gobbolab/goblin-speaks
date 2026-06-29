from .base import Activator
from src.config import Config
from gpiozero import Button


class GSButton(Activator):
    """
    A GPIO button/sensor activator backed by gpiozero's Button class.
    Compatible with any component that signals via a digital GPIO pin:
    physical buttons, IR beam sensors, reed switches, etc.
    """
    def __init__(self, config_prefix=None):
        config = Config()
        prefix = config_prefix or 'activator.gs_button'
        print("Values Loaded:")
        self.trigger_pin = config.get(f'{prefix}.trigger_pin', 21)
        print(f"Trigger Pin: {self.trigger_pin}")
        self.sensor = Button(self.trigger_pin, pull_up=True)

    def start(self, callback):
        print(f"Initializing GSButton activator on pin {self.trigger_pin}...")
        # Note: Depending on your specific component model and wiring, you may need to
        # change this to `when_released = callback` if it triggers when the signal is restored.
        self.sensor.when_pressed = callback
        print("GSButton Activator is ready. Waiting for trigger...")

    def shutdown(self):
        self.sensor.close()
        del self.sensor
        print("GSButton Activator is shut down.")
