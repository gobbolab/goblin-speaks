from src.config import Config
from src.plugin_loader import PluginLoader
from .gs_body import GSBody
from .base import Animatronic

class AnimatronicFactory:
    """Factory for creating animatronic instances based on configuration"""

    _animatronics = {
        'gs_body': GSBody,
    }

    @staticmethod
    def create(animatronic_type: str = None, config_prefix: str = None) -> object:
        config = Config()

        if animatronic_type is None:
            animatronic_type = config.get('animatronic.type', 'gs_body')

        if animatronic_type in AnimatronicFactory._animatronics:
            animatronic_class = AnimatronicFactory._animatronics[animatronic_type]
            return animatronic_class(config_prefix=config_prefix)

        plugins = PluginLoader.load_plugins('animatronic', Animatronic)
        if animatronic_type in plugins:
            return plugins[animatronic_type](config_prefix=config_prefix)

        raise ValueError(
            f"Unknown animatronic type: '{animatronic_type}'. "
            f"Built-in: {list(AnimatronicFactory._animatronics.keys())}. "
            f"Plugins: {list(plugins.keys())}"
        )