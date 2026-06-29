import board
import motor
from src.config import Config
from dispenser.base import Dispenser

class SingleStepperDispenser(Dispenser):
    def __init__(self, config_prefix=None):
        if config_prefix is None:
            super().__init__()
            prefix = 'dispenser.single_stepper'
        else:
            super().__init__(config_prefix)
            prefix = config_prefix

        config = Config()

        def get_conf(key, default):
            return config.get(f'{prefix}.{key}', default)
        
        pin1 = get_conf('pin_1', board.D17)
        pin2 = get_conf('pin_2', board.D18)
        pin3 = get_conf('pin_3', board.D27)
        pin4 = get_conf('pin_4', board.D22)
        self.dispense_steps = get_conf('dispense_steps', 2048)
        self.retract_steps  = get_conf('retract_steps', 512)
        self.step_delay     = get_conf('step_delay', 0.002)

        self.motor = motor.Stepper(pin1, pin2, pin3, pin4)

        print(f"Pin_1: {pin1}")
        print(f"Pin_2: {pin2}")
        print(f"Pin_3: {pin3}")
        print(f"Pin_4: {pin4}")
        print(f"Dispense Steps: {self.dispense_steps}")
        print(f"Retract Steps: {self.retract_steps}")
        print(f"Delay: {self.step_delay}")
        print("")
        

    def _dispense_one(self):
        """
        Performs a single dispense.
        """
        print("Dispensing...")
        self.motor.move_backward(self.dispense_steps, self.step_delay)
        self.motor.move_forward(self.retract_steps, self.step_delay)

    def step(self, steps):
        """
        Move the dispenser motor a set number of steps
        """
        print("Stepping dispenser motor...")
        self.motor.move_backward(steps)