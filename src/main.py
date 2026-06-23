import time
import typer
import pygame
import board
import digitalio
import subprocess
import sys
import dispenser
import animatronic
from audio_player import AudioPlayer
from version import __version__
from player import DefaultPlayer
from test_menu import TestMenu
from signal import pause
import activator

app = typer.Typer(help="Goblin Speaks fortune teller software")

@app.command()
def run():
    print("Not yet implemented. Shutting down...")
    player.shutdown()
    exit(0)

@app.command()
def test():
    menu = TestMenu(player)
    menu.run()
    player.shutdown()
    exit(0)

@app.command()
def update():
    """
    Pulls the latest release of Goblin Speaks and runs the installer.
    """
    typer.secho("Starting update process...", fg=typer.colors.CYAN)
    
    install_cmd = "curl -sL https://raw.githubusercontent.com/gobbolab/goblin-speaks/main/linux/setup.sh | sudo bash"
    
    try:
        subprocess.run(install_cmd, shell=True, check=True)
        typer.secho("Update successfully applied!", fg=typer.colors.GREEN)
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        typer.secho(f"The update script failed with exit code {e.returncode}.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    audio_player = AudioPlayer()
    animatronic_instance = animatronic.AnimatronicFactory.create()
    dispenser_instance = dispenser.DispenserFactory.create()
    activator_instance = activator.ActivatorFactory.create()
    
    player = DefaultPlayer(audio_player, animatronic_instance, dispenser_instance, activator_instance)

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