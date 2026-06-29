import os
import random

import pygame


VALID_MODES = ('sequential', 'random')


class SoundBank:
    def __init__(self, name: str, directory: str, mode: str = "sequential"):
        if mode not in VALID_MODES:
            raise ValueError(
                f"Sound bank '{name}' has invalid mode '{mode}'. "
                f"Must be one of: {', '.join(VALID_MODES)}"
            )

        self.name = name
        self.mode = mode
        self._sounds, self._name_to_sound = self._load_sounds(directory)
        self._index = 0

    def _load_sounds(self, directory):
        print(f"Loading sounds from {directory}...")
        sound_list = []
        name_to_sound = {}
        if not os.path.isdir(directory):
            print(f"  Directory not found: {directory}, creating it.")
            os.makedirs(directory, exist_ok=True)
            return sound_list, name_to_sound
        for filename in sorted(os.listdir(directory)):
            if filename.lower().endswith(('.mp3', '.wav')):
                try:
                    loaded = pygame.mixer.Sound(os.path.join(directory, filename))
                    sound_list.append(loaded)
                    stem = os.path.splitext(filename)[0]
                    if stem in name_to_sound:
                        print(f"  Warning: duplicate stem '{stem}' in bank '{self.name}', overwriting")
                    name_to_sound[filename] = loaded
                    name_to_sound[stem] = loaded
                    print(f"  Loaded: {filename}")
                except pygame.error as e:
                    print(f"  Error loading {filename}: {e}")
        return sound_list, name_to_sound

    def get_sound(self):
        if not self._sounds:
            return None
        if self.mode == 'random':
            return random.choice(self._sounds)

        sound = self._sounds[self._index]
        self._index = (self._index + 1) % len(self._sounds)
        return sound

    def get_sound_by_name(self, name: str):
        return self._name_to_sound.get(name)

    @property
    def sound_names(self) -> list[str]:
        return [os.path.splitext(f)[0] for f in self._name_to_sound if '.' in f]

    def __len__(self):
        return len(self._sounds)
