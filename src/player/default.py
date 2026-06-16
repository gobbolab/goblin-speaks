from .base import BasePlayer

class DefaultPlayer(BasePlayer):
    def play(self):
        """
        Executes one play of the machine.
        1. Selects an audio file to play at random
        2. Activates the animatronic
        3. Dispenses card when audio complete
        """
        print("Starting play...")
        duration = self.audio_player.play_random()
        self.animatronic.animate(duration)
        print("Audio/animations complete...")
        self.dispenser.dispense()
        print("Play finished.")

