import board
import motor
from src.config import Config
from dispenser.base import Dispenser

class GSCardDispenser(Dispenser):
    def __init__(self, *args, **kwargs):
        """
        Initializes the GS Card Dispenser with 4 specific hardware pins.
        """
        config = Config()
        
        pin1 = config.get('dispenser.gs_card.pin_1', board.D17)
        pin2 = config.get('dispenser.gs_card.pin_2', board.D18)
        pin3 = config.get('dispenser.gs_card.pin_3', board.D27)
        pin4 = config.get('dispenser.gs_card.pin_4', board.D22)

        self.motor = motor.Stepper(pin1, pin2, pin3, pin4)
        self.steps = config.get('dispenser.gs_card.steps', 2048)
        self.delay = config.get('dispenser.gs_card.delay', 0.002)

        
        print("=== Dispenser GS_Card Initialized ===")
        print("Values Loaded:")
        print(f"Pin_1: {pin1}")
        print(f"Pin_2: {pin2}")
        print(f"Pin_3: {pin3}")
        print(f"Pin_4: {pin4}")
        print(f"Steps:" {self.steps})
        print(f"Delay:" {self.delay})
        print("")
        

    def dispense(self):
        """
        Dispenses a fortune card.
        """
        print("Dispensing card...")
        self.motor.move_backward(self.steps, self.delay)

    def step(self, steps):
        """
        Move the dispenser motor a set number of steps
        """
        print("Stepping dispenser motor...")
        self.motor.move_backward(steps)