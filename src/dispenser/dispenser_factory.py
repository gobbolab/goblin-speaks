from src.config import Config
from src.plugin import PluginLoader
from .single_stepper import SingleStepperDispenser
from .base import Dispenser

class DispenserFactory:
    """Factory for creating dispenser instances based on configuration"""

    _dispensers = {
        'single_stepper': SingleStepperDispenser,
    }

    @staticmethod
    def create(dispenser_type: str = None, config_prefix: str = None) -> object:
        config = Config()

        if dispenser_type is None:
            dispenser_type = config.get('dispenser.type', 'single_stepper')

        if dispenser_type in DispenserFactory._dispensers:
            dispenser_class = DispenserFactory._dispensers[dispenser_type]
            return dispenser_class(config_prefix=config_prefix)

        plugins = PluginLoader.load_plugins('dispenser', Dispenser)
        if dispenser_type in plugins:
            return plugins[dispenser_type](config_prefix=config_prefix)

        raise ValueError(
            f"Unknown dispenser type: '{dispenser_type}'. "
            f"Built-in: {list(DispenserFactory._dispensers.keys())}. "
            f"Plugins: {list(plugins.keys())}"
        )