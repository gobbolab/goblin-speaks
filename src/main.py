import typer
import time
import pygame
import board
import digitalio
import dispenser
import animatronic
from audio_player import AudioPlayer
from version import __version__

audio_player = AudioPlayer()

animatronic = animatronic.GSBody(0, 1)
card = dispenser.GSCardDispenser(board.D17, board.D18, board.D19, board.D20)

app = typer.Typer(help="Goblin Speaks fortune teller software")

def play():
    """
    Executes one play of the machine.
    1. Selects an audio file to play at random
    2. Activates the animatronic
    3. Dispenses card when audio complete
    """
    print("Starting play...")

    duration = audio_player.playrandom()
    animatronic.animate(duration)

    print("Audio/animations complete...")
    
    card.dispense()

    print("Play finished.")

def run_test_menu():
    while True:
        print("\nMenu:")
        print("1. Play")
        print("2. Test Card")
        print("3. Test Audio")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Starting play...")
            # play()
        elif choice == "2":
            print("Testing card dispenser...")
            card.dispense()
        elif choice == "3":
            print("Testing voice...")
            # play_voice()
        elif choice == "0":
            print("Exiting...")
            return
        else:
            print("Invalid input.")

@app.command()
def run():
    typer.echo("Application is running!")

@app.command()
def test():
    run_test_menu()

if __name__ == "__main__":
    print(f"Goblin Speaks Fortune Teller Framework - {__version__}")
    app()