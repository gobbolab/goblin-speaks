from .base import Activator
from src.config import Config
from gpiozero import Button

class GSCoin(Activator):
    def __init__(self):
        config = Config()
        self.trigger_pin = config.get('activator.gs_coin.trigger_pin', 21)
        self.sensor = Button(self.trigger_pin, pull_up=True)

    def start(self, callback):
        print(f"Initializing IR sensor on pin {self.trigger_pin}...")
        # Note: Depending on your specific IR sensor model and wiring, you may need to
        # change this to `when_released = callback` if it triggers when the beam is restored.
        self.sensor.when_pressed = callback
        print("GS_Coin Activator is ready. Waiting for IR trigger...")

    def shutdown(self):
        self.sensor.close()
        del self.sensor
        print("GS_Coin Activator is shut down.")
