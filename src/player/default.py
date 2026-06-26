from .base import BasePlayer
from audio_player import SoundType

class DefaultPlayer(BasePlayer):
    def play(self):
        """
        Executes one play of the machine.
        1. Plays pre-show, show, and post-show sounds in sequence
        2. Animates the animatronic for the total audio duration
        3. Dispenses a card once audio and animation are complete
        """
        print("Starting play...")
        duration = self.audio_player.play_sequence([
            SoundType.PRE_SHOW,
            SoundType.SHOW,
            SoundType.POST_SHOW,
        ])
        self.animatronic.animate(duration)
        print("Audio/animations complete...")
        self.dispenser.dispense()
        print("Play finished.")


