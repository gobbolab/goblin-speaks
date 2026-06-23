import typer
import sys
import dispenser
import animatronic
from audio_player import AudioPlayer
from version import __version__
from update import perform_update
from player import DefaultPlayer
from test_menu import TestMenu
import activator

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
    menu = TestMenu(player)
    menu.run()
    player.shutdown()
    sys.exit(0)

@app.command()
def update():
    """
    Pulls the latest release of Goblin Speaks and runs the installer.
    """
    perform_update()

def load_player():
    audio_player = AudioPlayer()
    animatronic_instance = animatronic.AnimatronicFactory.create()
    dispenser_instance = dispenser.DispenserFactory.create()
    activator_instance = activator.ActivatorFactory.create()

    return DefaultPlayer(audio_player, animatronic_instance, dispenser_instance, activator_instance)

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
    print(f"Fortune Teller Framework - {__version__}")

    app()