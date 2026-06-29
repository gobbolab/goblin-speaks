import time
from abc import ABC, abstractmethod
from src.config import Config


class Dispenser(ABC):
    def __init__(self, config_prefix=None):
        config = Config()
        prefix = config_prefix or 'dispenser'
        self.dispense_delay = config.get(f'{prefix}.dispense_delay', 1.0)
        print("Values Loaded:")
        print(f"Dispense Delay: {self.dispense_delay}")

    def dispense(self, count: int = 1):
        """
        Dispenses one or more items, with a configurable delay between each.
        Subclasses implement _dispense_one() for the actual dispense logic.
        """
        for i in range(count):
            self._dispense_one()
            if count > 1 and i < count - 1:
                time.sleep(self.dispense_delay)

    @abstractmethod
    def _dispense_one(self):
        """
        Performs a single dispense action.
        Must be implemented by all concrete subclasses.
        """
        pass

    def test(self):
        raw = input("Number of items to dispense [1]: ").strip()
        count = int(raw) if raw else 1
        self.dispense(count)

    def step(self, steps):
        """
        Move the dispenser mechanism a set number of steps.
        May be overridden by concrete subclasses that support it.
        """
        pass