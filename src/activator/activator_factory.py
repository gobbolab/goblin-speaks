from src.config import Config
from src.plugin import PluginLoader
from .gpiozero_button import GpioZeroButton
from .base import Activator

class ActivatorFactory:
    """Factory for creating activator instances based on configuration"""

    _activators = {
        'gpiozero_button': GpioZeroButton,
    }

    @staticmethod
    def create(activator_type: str = None, config_prefix: str = None) -> object:
        config = Config()

        if activator_type is None:
            activator_type = config.get('activator.type', 'gpiozero_button')

        if activator_type in ActivatorFactory._activators:
            activator_class = ActivatorFactory._activators[activator_type]
            print(f"Creating activator: {activator_type}")
            return activator_class(config_prefix=config_prefix)

        plugins = PluginLoader.load_plugins('activator', Activator)
        if activator_type in plugins:
            print(f"Creating activator from plugin: {activator_type}")
            return plugins[activator_type](config_prefix=config_prefix)

        raise ValueError(
            f"Unknown activator type: '{activator_type}'. "
            f"Built-in: {list(ActivatorFactory._activators.keys())}. "
            f"Plugins: {list(plugins.keys())}"
        )

    @staticmethod
    def create_all() -> list:
        config = Config()
        activators_config = config.get('activators', {})
        result = []
        for name, act_config in activators_config.items():
            act_type = act_config.get('type')
            sequence_name = act_config.get('sequence')
            if not sequence_name:
                raise ValueError(f"Activator '{name}' is missing a 'sequence' field")
            activator = ActivatorFactory.create(act_type, config_prefix=f'activators.{name}')
            result.append((activator, sequence_name))
        return result
