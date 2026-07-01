from dispenser.base import Dispenser
from activator.base import Activator
from animatronic.base import Animatronic
from .loader import PluginLoader
from .generator import PluginGenerator

_BASE_CLASS_MAP = {
    'dispenser': Dispenser,
    'activator': Activator,
    'animatronic': Animatronic,
}

def create_plugin(component_type: str, name: str):
    """Create a new plugin skeleton file for the given component type and name."""
    if component_type not in _BASE_CLASS_MAP:
        raise ValueError(f"Unknown component type: '{component_type}'. Available: {list(_BASE_CLASS_MAP.keys())}")

    base_class = _BASE_CLASS_MAP[component_type]
    plugin_dir = PluginLoader._get_plugin_dir() / component_type
    plugin_file = plugin_dir / f"{name}.py"

    if plugin_file.exists():
        raise FileExistsError(f"Plugin already exists: {plugin_file}")

    plugin_dir.mkdir(parents=True, exist_ok=True)

    skeleton = PluginGenerator.generate_skeleton(base_class, name)
    plugin_file.write_text(skeleton)
    print(f"Created plugin skeleton: {plugin_file}")
