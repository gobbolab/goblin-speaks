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
from plugin import create_plugin
from activator import ActivatorFactory
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

@app.command()
def plugin(component_type: str, name: str):
    """Create a new plugin skeleton file. Usage: goblin-speaks plugin dispenser my_dispenser"""
    try:
        create_plugin(component_type, name)
    except (ValueError, FileExistsError) as e:
        print(e)
        sys.exit(1)

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