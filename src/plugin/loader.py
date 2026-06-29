import importlib.util
import inspect
import sys
from pathlib import Path
from src.config import Config


class PluginLoader:
    _plugins = {}

    @staticmethod
    def _get_plugin_dir():
        config = Config()
        default = Path.home() / '.goblin-speaks' / 'plugins'
        return Path(config.get('plugins.directory', str(default)))

    @classmethod
    def load_plugins(cls, component_type, base_class):
        """
        Scans the plugins directory for user-provided component implementations.

        Looks in <plugins_dir>/<component_type>/ for .py files, imports each one,
        and finds the first class that subclasses base_class. The filename (without
        .py) becomes the key used to reference the plugin in config.

        Results are cached per component_type so the filesystem is only scanned once.
        """

        # Return cached results if we've already scanned this component type
        if component_type in cls._plugins:
            return cls._plugins[component_type]

        plugins = {}
        plugin_dir = cls._get_plugin_dir() / component_type

        # If the directory doesn't exist, there are no plugins to load
        if not plugin_dir.is_dir():
            cls._plugins[component_type] = plugins
            return plugins

        # Scan each .py file in the plugin directory (skip files starting with _)
        for file_path in sorted(plugin_dir.glob('*.py')):
            if file_path.name.startswith('_'):
                continue

            module_name = file_path.stem
            try:
                # Dynamically import the plugin module
                spec = importlib.util.spec_from_file_location(
                    f"plugins.{component_type}.{module_name}", file_path
                )
                module = importlib.util.module_from_spec(spec)
                # Inject the base class and Config so plugins can use them
                # without importing from the framework's internal paths
                module.__dict__[base_class.__name__] = base_class
                module.__dict__['Config'] = Config
                sys.modules[spec.name] = module
                spec.loader.exec_module(module)

                # Find the first class in the module that extends the base class
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, base_class) and obj is not base_class:
                        plugins[module_name] = obj
                        print(f"Loaded plugin: {module_name} ({obj.__name__})")
                        break
            except Exception as e:
                print(f"Warning: Failed to load plugin '{module_name}' from {file_path}: {e}")

        cls._plugins[component_type] = plugins
        return plugins

    @classmethod
    def reload(cls):
        cls._plugins.clear()
