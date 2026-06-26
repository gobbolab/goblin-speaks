from abc import ABC, abstractmethod
from audio_player import AudioPlayer
from animatronic.base import Animatronic
from dispenser.base import Dispenser
from activator.base import Activator

class BasePlayer(ABC):
    def __init__(self, audio_player: AudioPlayer, animatronic: Animatronic, dispenser: Dispenser, activator: Activator):
        self.audio_player = audio_player
        self.animatronic = animatronic
        self.dispenser = dispenser
        self.activator = activator

    @abstractmethod
    def play(self):
        pass

    def test_animatronic(self):
        self.animatronic.test()

    def test_dispenser(self):
        self.dispenser.dispense()

    def step_dispenser(self):
        self.dispenser.step(10)

    def test_audio(self):
        self.audio_player.play_show_sound()

    def test_activator(self):
        print("Testing activator... waiting for trigger.")
        def _callback():
            print("\n*** Activator triggered successfully! ***\n")
        self.activator.start(_callback)

    def shutdown(self):
        self.activator.shutdown()
        
