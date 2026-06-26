import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from src.config import Config

class AudioPlayer:
    def __init__(self):
        config = Config()
        
        self.activation_sound_dir = config.get('audio_player.activation_sound_dir', '/opt/goblin-speaks/sounds/activation')
        self.show_sound_dir = config.get('audio_player.show_sound_dir', '/opt/goblin-speaks/sounds/show')
        self.show_sound_mode = config.get('audio_player.show_sound_mode', 'sequential')
        self.activation_sound_mode = config.get('audio_player.activation_sound_mode', 'sequential')

        pygame.mixer.pre_init(44100, -16, 1, 2048)
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.show_sound_list = self._load_sounds(self.show_sound_dir)
        self.activation_sound_list = self._load_sounds(self.activation_sound_dir)

        # Initialize indices for sequential mode
        self.show_sound_index = 0
        self.activation_sound_index = 0

        print(f"Loading complete.\nShow sounds: {len(self.show_sound_list)}\nActivation sounds: {len(self.activation_sound_list)}")

    def _load_sounds(self, directory):
        sound_list = []
        for filename in os.listdir(directory):
            if filename.lower().endswith('.mp3'):
                try:
                    loaded = pygame.mixer.Sound(os.path.join(directory, filename))
                    sound_list.append(loaded)
                    print(f"Loaded: {filename}")
                except pygame.error as e:
                    print(f"Error loading {filename}: {e}")
        return sound_list

    def play_show_sound(self):
        """
        Plays a sound based on the show sound mode.
        Returns the duration of the sound being played.
        This call is non blocking.
        """
        if not self.show_sound_list:
            print("Warning: No show sounds loaded to play.")
            return 0.0
        
        if self.show_sound_mode == 'random':
            sound = random.choice(self.show_sound_list)
        else:
            sound = self.show_sound_list[self.show_sound_index]
            self.show_sound_index = (self.show_sound_index + 1) % len(self.show_sound_list)


        duration = sound.get_length()        
        sound.play()

        return duration

    def play_activation_sound(self):
        """
        Plays a sound based on the activation sound mode.
        Returns the duration of the sound being played.
        This call is non blocking.
        """
        if not self.activation_sound_list:
            print("Warning: No activation sounds loaded to play.")
            return 0.0
        
        if self.activation_sound_mode == 'random':
            sound = random.choice(self.activation_sound_list)
        else:
            sound = self.activation_sound_list[self.activation_sound_index]
            self.activation_sound_index = (self.activation_sound_index + 1) % len(self.activation_sound_list)

        duration = sound.get_length()        
        sound.play()

        return duration
