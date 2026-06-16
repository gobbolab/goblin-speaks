import typer
import pygame
import board
import digitalio
import dispenser
import animatronic
from audio_player import AudioPlayer
from version import __version__
from player import DefaultPlayer
from test_menu import TestMenu

app = typer.Typer(help="Goblin Speaks fortune teller software")

@app.command()
def run():
    typer.echo("Run mode not implemented")

@app.command()
def test():
    menu = TestMenu(player)
    menu.run()

if __name__ == "__main__":
    audio_player = AudioPlayer()
    animatronic_instance = animatronic.AnimatronicFactory.create()
    dispenser_instance = dispenser.DispenserFactory.create()
    
    player = DefaultPlayer(audio_player, animatronic_instance, dispenser_instance)

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