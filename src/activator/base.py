from abc import ABC, abstractmethod

class Activator(ABC):
    @abstractmethod
    def start(self, callback):
        """
        Abstract method to start the activator and bind a callback.
        """
        pass
