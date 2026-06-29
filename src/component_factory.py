from src.config import Config
from animatronic import AnimatronicFactory
from dispenser import DispenserFactory
from activator import ActivatorFactory
from terminal_helper import print_header


_FACTORY_MAP = {
    'animatronic': AnimatronicFactory,
    'dispenser': DispenserFactory,
    'activator': ActivatorFactory,
}


class ComponentFactory:

    @staticmethod
    def create_all() -> dict:
        config = Config()
        components_config = config.get('components', {})

        if not components_config:
            raise ValueError("No 'components' section found in config")

        print_header("LOADING COMPONENTS")

        components = {}
        for name, comp_config in components_config.items():
            comp_type = comp_config.get('type')
            if not comp_type:
                raise ValueError(f"Component '{name}' is missing a 'type' field")

            if comp_type not in _FACTORY_MAP:
                raise ValueError(
                    f"Component '{name}' has unknown type '{comp_type}'. "
                    f"Available: {', '.join(_FACTORY_MAP.keys())}"
                )

            factory = _FACTORY_MAP[comp_type]
            comp_class = comp_config.get('class')
            if not comp_class:
                raise ValueError(
                    f"Component '{name}' (type: {comp_type}) is missing a 'class' field"
                )

            config_prefix = f'components.{name}'
            print(f"Creating component '{name}' (type: {comp_type}, class: {comp_class})")
            components[name] = factory.create(comp_class, config_prefix=config_prefix)

        return components
