from abc import ABC, abstractmethod

class Dispenser(ABC):
    @abstractmethod
    def dispense(self):
        """
        Abstract method that must be overridden by all concrete subclasses.
        """
        pass