import signal
import typer
import sys
from audio import AudioPlayer
from version import __version__
from update import perform_update
from player import SequencePlayer
from sequence_test_menu import SequenceTestMenu
from component_factory import ComponentFactory
from config import Config
from plugin import PluginLoader, PluginGenerator
from dispenser.base import Dispenser
from activator.base import Activator
from activator import ActivatorFactory
from animatronic.base import Animatronic
from terminal_helper import print_logo

app = typer.Typer(help="Goblin Speaks fortune teller software")

@app.command()
def run():
    player = load_player()
    activators = load_activators(player)
    if not activators:
        print("No activators configured. Shutting down...")
        player.shutdown()
        sys.exit(1)
    print("Ready. Waiting for activation...")
    try:
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        for activator in activators:
            activator.shutdown()
        player.shutdown()

@app.command()
def menu():
    player = load_player()
    menu = SequenceTestMenu(player)
    menu.run()
    player.shutdown()
    sys.exit(0)

@app.command()
def update():
    """
    Pulls the latest release of Goblin Speaks and runs the installer.
    """
    perform_update()

_BASE_CLASS_MAP = {
    'dispenser': Dispenser,
    'activator': Activator,
    'animatronic': Animatronic,
}

@app.command()
def plugin(component_type: str, name: str):
    """Create a new plugin skeleton file. Usage: goblin-speaks plugin dispenser my_dispenser"""
    if component_type not in _BASE_CLASS_MAP:
        print(f"Unknown component type: '{component_type}'. Available: {list(_BASE_CLASS_MAP.keys())}")
        sys.exit(1)

    base_class = _BASE_CLASS_MAP[component_type]
    plugin_dir = PluginLoader._get_plugin_dir() / component_type
    plugin_file = plugin_dir / f"{name}.py"

    if plugin_file.exists():
        print(f"Plugin already exists: {plugin_file}")
        sys.exit(1)

    plugin_dir.mkdir(parents=True, exist_ok=True)

    skeleton = PluginGenerator.generate_skeleton(base_class, name)
    plugin_file.write_text(skeleton)
    print(f"Created plugin skeleton: {plugin_file}")

def load_player():
    components = ComponentFactory.create_all()
    components['audio'] = AudioPlayer()
    return SequencePlayer(components)

def load_activators(player: SequencePlayer) -> list:
    config = Config()
    activators_config = config.get('activators', {})
    activators = []
    for name, act_config in activators_config.items():
        act_type = act_config.get('type')
        sequence_name = act_config.get('sequence')
        if not sequence_name:
            raise ValueError(f"Activator '{name}' is missing a 'sequence' field")
        if sequence_name not in player.sequence_names:
            raise ValueError(
                f"Activator '{name}' references unknown sequence '{sequence_name}'. "
                f"Available: {player.sequence_names}"
            )
        activator = ActivatorFactory.create(act_type, config_prefix=f'activators.{name}')
        activator.start(lambda sn=sequence_name: player.play(sn))
        activators.append(activator)
    return activators

if __name__ == "__main__":
    print_logo(__version__)

    app()