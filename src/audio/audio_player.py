import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from src.config import Config
from audio.sound_bank import SoundBank
from terminal_helper import print_header


class AudioPlayer:
    def __init__(self):
        config = Config()

        sounds_dir = config.get('audio_player.sounds_dir', '~/.goblin-speaks/sounds')
        sounds_dir = os.path.expanduser(sounds_dir)

        banks_config = config.get('audio_player.sound_banks', {})

        print("")
        print_header("LOADING AUDIO PLAYER")
        print(f"Sounds directory: {sounds_dir}")

        pygame.mixer.pre_init(44100, -16, 1, 2048)
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self._banks = self._init_banks(banks_config, sounds_dir)

        print("Loading complete.")
        for name, bank in self._banks.items():
            print(f"  {name}: {len(bank)} sounds")
        print("")

    @property
    def bank_names(self) -> list[str]:
        return list(self._banks.keys())

    def _init_banks(self, banks_config, sounds_dir) -> dict[str, SoundBank]:
        banks = {}
        for bank_name, bank_conf in banks_config.items():
            bank_conf = bank_conf or {}
            bank_dir = os.path.join(sounds_dir, bank_name)
            mode = bank_conf.get('mode', 'sequential')
            banks[bank_name] = SoundBank(bank_name, bank_dir, mode)
        return banks

    def play(self, bank_name: str, file_name: str = None, block: bool = False) -> float:
        """
        Plays a sound from the specified sound bank.
        If file_name is given, plays that specific file; otherwise plays the next sound.
        If block is True, waits for the sound to finish before returning.
        Returns the duration of the sound in seconds.
        """
        import time

        bank = self._banks.get(bank_name)
        if bank is None:
            print(f"Warning: Unknown sound bank '{bank_name}'.")
            return 0.0

        if file_name is not None:
            sound = bank.get_sound_by_name(file_name)
            if sound is None:
                print(f"Warning: Sound '{file_name}' not found in bank '{bank_name}'.")
                return 0.0
        else:
            sound = bank.get_sound()
            if sound is None:
                print(f"Warning: No sounds loaded in bank '{bank_name}'.")
                return 0.0

        duration = sound.get_length()
        sound.play()
        if block:
            time.sleep(duration)
        return duration

    def play_sequence(self, sound_types: list[str], block: bool = False) -> float:
        """
        Plays a sequence of sound banks in order.
        If block is True, plays on the current thread (blocking).
        Otherwise plays on a background thread and returns immediately.
        Returns the total duration in seconds.
        """
        import threading
        import time

        selected = []
        for bank_name in sound_types:
            bank = self._banks.get(bank_name)
            if bank is None:
                print(f"Warning: Unknown sound bank '{bank_name}', skipping.")
                continue
            sound = bank.get_sound()
            if sound is not None:
                selected.append(sound)

        total_duration = sum(s.get_length() for s in selected)

        def _run():
            for sound in selected:
                sound.play()
                time.sleep(sound.get_length())

        if selected:
            if block:
                _run()
            else:
                thread = threading.Thread(target=_run, daemon=True)
                thread.start()

        return total_duration
