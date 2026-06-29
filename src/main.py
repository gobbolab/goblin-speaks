import typer
import sys
from audio_player import AudioPlayer
from version import __version__
from update import perform_update
from player import SequencePlayer
from sequence_test_menu import SequenceTestMenu
from component_factory import ComponentFactory
from plugin import PluginLoader, PluginGenerator
from dispenser.base import Dispenser
from activator.base import Activator
from animatronic.base import Animatronic

app = typer.Typer(help="Goblin Speaks fortune teller software")

@app.command()
def run():
    player = load_player()
    print("Not yet implemented. Shutting down...")
    player.shutdown()
    sys.exit(0)

@app.command()
def test():
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

if __name__ == "__main__":
    print(r"""
     _____       _     _ _         _____                  _        
    |  __ \     | |   | (_)       /  ___|                | |       
    | |  \/ ___ | |__ | |_ _ __   \ `--. _ __   ___  __ _| | _____ 
    | | __ / _ \| '_ \| | | '_ \   `--. \ '_ \ / _ \/ _` | |/ / __|
    | |_\ \ (_) | |_) | | | | | | /\__/ / |_) |  __/ (_| |   <\__ \
     \____/\___/|_.__/|_|_|_| |_| \____/| .__/ \___|\__,_|_|\_\___/
                                        | |                        
                                        |_|                        
          """)
    print(f"                Penny Arcade Framework - {__version__}")
    print("")

    app()