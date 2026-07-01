import signal
import typer
import sys
from audio import AudioPlayer
from version import __version__
from update import perform_update
from sequence_player import SequencePlayer
from sequence_test_menu import SequenceTestMenu
from component_factory import ComponentFactory
from plugin import create_plugin
from activator import ActivatorFactory
from terminal_helper import print_logo

app = typer.Typer(help="Goblin Speaks fortune teller software")

@app.command()
def run():
    player = load_player()
    if not player.activators:
        print("No activators configured. Shutting down...")
        player.shutdown()
        sys.exit(1)
    print("Ready. Waiting for activation...")
    try:
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
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

@app.command()
def plugin(component_type: str, name: str):
    """Create a new plugin skeleton file. Usage: goblin-speaks plugin dispenser my_dispenser"""
    try:
        create_plugin(component_type, name)
    except (ValueError, FileExistsError) as e:
        print(e)
        sys.exit(1)

def load_player():
    activators = ActivatorFactory.create_all()
    components = ComponentFactory.create_all()
    components['audio'] = AudioPlayer()
    return SequencePlayer(components, activators)

if __name__ == "__main__":
    print_logo(__version__)

    app()