import board
import motor
from dispenser.base import Dispenser

class GSCardDispenser(Dispenser):
    def __init__(self, pin1, pin2, pin3, pin4, *args, **kwargs):
        """
        Initializes the GS Card Dispenser with 4 specific hardware pins.
        """
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4

        self.motor = motor.Stepper(pin1, pin2, pin3, pin4)

    def dispense(self):
        """
        Dispenses a fortune card.
        """
        print("Dispensing card...")
        self.motor.move_backward(2800)