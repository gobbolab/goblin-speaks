import time
import board
import digitalio

class Stepper:
    """Control a stepper motor using 4 pins."""
    
    def __init__(self, pin1, pin2, pin3, pin4):
        """
        Initialize stepper with 4 control pins.
        
        Args:
            pin1, pin2, pin3, pin4: Board pins for stepper control
        """
        self.pins = [
            digitalio.DigitalInOut(pin1),
            digitalio.DigitalInOut(pin2),
            digitalio.DigitalInOut(pin3),
            digitalio.DigitalInOut(pin4)
        ]
        
        for pin in self.pins:
            pin.direction = digitalio.Direction.OUTPUT
        
        # Stepper sequence for full step
        self.sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
        self.step_index = 0
    
    def move_forward(self, steps, delay=0.002):
        """Move stepper forward by N steps."""
        for _ in range(steps):
            self._set_pins(self.sequence[self.step_index])
            self.step_index = (self.step_index + 1) % len(self.sequence)
            time.sleep(delay)
        self._cleanup()
    
    def move_backward(self, steps, delay=0.002):
        """Move stepper backward by N steps."""
        for _ in range(steps):
            self.step_index = (self.step_index - 1) % len(self.sequence)
            self._set_pins(self.sequence[self.step_index])
            time.sleep(delay)
        self._cleanup()
    
    def _set_pins(self, state):
        """Set all pins to the given state."""
        for i, pin in enumerate(self.pins):
            pin.value = bool(state[i])

    def _cleanup(self):
        """Set all pins to LOW."""
        for pin in self.pins:
            pin.value = False