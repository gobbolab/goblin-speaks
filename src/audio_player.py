import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class AudioPlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.sound_list = []

        print("Loading sounds...")
        
        for filename in os.listdir('.'):
            if filename.lower().endswith('.mp3'):
                try:
                    loaded = pygame.mixer.Sound(filename)
                    self.sound_list.append(loaded)
                    print(f"Loaded: {filename}")
                except pygame.error as e:
                    print(f"Error loading {filename}: {e}")

        print(f"Loading complete.\nLoaded {len(self.sound_list)} sounds.\n")


    def play_random(self):
        """
        Plays a random sound file from the sound list.
        Returns the duration of the of the sound being played.
        This call is non blocking.
        """
        if not self.sound_list:
            print("Warning: No sounds loaded to play.")
            return 0.0
        
        sound = random.choice(self.sound_list)
        duration = sound.get_length()        
        sound.play()

        return duration
        
        

# Example usage:
# if __name__ == "__main__":
#     player = AudioPlayer()
#     length = player.playrandom()
#     print(f"Playing a random sound. Duration: {length:.2f} seconds.")