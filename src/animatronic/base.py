# animatronic/base.py
from abc import ABC, abstractmethod

class Animatronic(ABC):
    @abstractmethod
    def animate(self, duration: float):
        """
        Abstract method to animate the animatronic for a specific duration.
        """
        pass

    @abstractmethod
    def test(self):
        """
        Abstract method to run a diagnostic test on the animatronic.
        """
        pass