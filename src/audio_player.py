import os
import random
from dataclasses import dataclass, field
from enum import Enum

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from src.config import Config


class SoundType(Enum):
    PRE_SHOW = "pre_show"
    SHOW = "show"
    POST_SHOW = "post_show"
    ACTIVATION = "activation"


@dataclass
class _SoundBank:
    sounds: list = field(default_factory=list)
    mode: str = "sequential"
    index: int = 0


class AudioPlayer:
    def __init__(self):
        config = Config()

        def get_conf(key, default):
            return config.get(f'audio_player.{key}', default)

        # --- Config ---
        pre_show_dir   = get_conf('pre_show_sound_dir',   '/opt/goblin-speaks/sounds/pre_show')
        show_dir       = get_conf('show_sound_dir',       '/opt/goblin-speaks/sounds/show')
        post_show_dir  = get_conf('post_show_sound_dir',  '/opt/goblin-speaks/sounds/post_show')
        activation_dir = get_conf('activation_sound_dir', '/opt/goblin-speaks/sounds/activation')

        pre_show_mode   = get_conf('pre_show_sound_mode',   'sequential')
        show_mode       = get_conf('show_sound_mode',       'sequential')
        post_show_mode  = get_conf('post_show_sound_mode',  'sequential')
        activation_mode = get_conf('activation_sound_mode', 'sequential')

        print("Initializing Audio Player")
        print("Values Loaded:")
        print(f"Pre-Show Sound Dir: {pre_show_dir}")
        print(f"Pre-Show Sound Mode: {pre_show_mode}")
        print(f"Show Sound Dir: {show_dir}")
        print(f"Show Sound Mode: {show_mode}")
        print(f"Post-Show Sound Dir: {post_show_dir}")
        print(f"Post-Show Sound Mode: {post_show_mode}")
        print(f"Activation Sound Dir: {activation_dir}")
        print(f"Activation Sound Mode: {activation_mode}")
        print("")

        pygame.mixer.pre_init(44100, -16, 1, 2048)
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        print("Loading pre-show sounds...")
        print("Loading show sounds...")
        print("Loading post-show sounds...")
        print("Loading activation sounds...")

        self._banks: dict[SoundType, _SoundBank] = {
            SoundType.PRE_SHOW:   _SoundBank(self._load_sounds(pre_show_dir),   pre_show_mode),
            SoundType.SHOW:       _SoundBank(self._load_sounds(show_dir),       show_mode),
            SoundType.POST_SHOW:  _SoundBank(self._load_sounds(post_show_dir),  post_show_mode),
            SoundType.ACTIVATION: _SoundBank(self._load_sounds(activation_dir), activation_mode),
        }

        print(
            f"Loading complete.\n"
            f"Pre-show sounds: {len(self._banks[SoundType.PRE_SHOW].sounds)}\n"
            f"Show sounds: {len(self._banks[SoundType.SHOW].sounds)}\n"
            f"Post-show sounds: {len(self._banks[SoundType.POST_SHOW].sounds)}\n"
            f"Activation sounds: {len(self._banks[SoundType.ACTIVATION].sounds)}\n"
        )

    def _load_sounds(self, directory):
        sound_list = []
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.mp3', '.wav')):
                try:
                    loaded = pygame.mixer.Sound(os.path.join(directory, filename))
                    sound_list.append(loaded)
                    print(f"Loaded: {filename}")
                except pygame.error as e:
                    print(f"Error loading {filename}: {e}")
        return sound_list

    def _select_sound(self, bank: _SoundBank):
        """
        Selects and returns the next sound from a bank according to its mode.
        Returns None if the bank is empty.
        """
        if not bank.sounds:
            return None
        if bank.mode == 'random':
            return random.choice(bank.sounds)
        else:
            sound = bank.sounds[bank.index]
            bank.index = (bank.index + 1) % len(bank.sounds)
            return sound

    def play(self, sound_type: SoundType) -> float:
        """
        Plays the next sound from the specified sound bank.
        Returns the duration of the sound in seconds.
        This call is non-blocking.
        """
        bank = self._banks[sound_type]
        sound = self._select_sound(bank)

        if sound is None:
            print(f"Warning: No {sound_type.value} sounds loaded to play.")
            return 0.0

        duration = sound.get_length()
        sound.play()
        return duration

    def play_sequence(self, sound_types: list[SoundType]) -> float:
        """
        Plays a sequence of sound banks in order on a background thread.
        Sounds are selected upfront; the total duration is returned immediately
        so the caller can start the animatronic before playback begins.
        Empty banks are skipped silently.
        This call is non-blocking.
        """
        import threading
        import time

        selected = []
        for sound_type in sound_types:
            sound = self._select_sound(self._banks[sound_type])
            if sound is not None:
                selected.append(sound)

        total_duration = sum(s.get_length() for s in selected)

        def _run():
            for i, sound in enumerate(selected):
                sound.play()
                time.sleep(sound.get_length())

        if selected:
            thread = threading.Thread(target=_run, daemon=True)
            thread.start()

        return total_duration
