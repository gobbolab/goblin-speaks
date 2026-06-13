# animatronic/gs_body.py
from .base import Animatronic
# Assuming you have a servo library available
from motor.servo import Servo 

class GSBody(Animatronic):
    def __init__(self, arm_pin, mouth_pin, *args, **kwargs):
        """
        Initializes the GSBody with arm and mouth servo pins.
        """

    def animate(self, duration: float):
        """
        Performs animation logic over the specified duration.
        """
        print(f"Animating body for {duration} seconds...")

    def test(self):
        """
        Runs a quick diagnostic sweep of the servos.
        """
        print("Testing arm and mouth servos...")
        return True