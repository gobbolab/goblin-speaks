from abc import ABC, abstractmethod
from audio_player import AudioPlayer
from animatronic.base import Animatronic
from dispenser.base import Dispenser

class BasePlayer(ABC):
    def __init__(self, audio_player: AudioPlayer, animatronic: Animatronic, dispenser: Dispenser):
        self.audio_player = audio_player
        self.animatronic = animatronic
        self.dispenser = dispenser

    @abstractmethod
    def play(self):
        pass

    def test_animatronic(self):
        self.animatronic.test()

    def test_dispenser(self):
        self.dispenser.dispense()

    def test_audio(self):
        self.audio_player.play_random()
