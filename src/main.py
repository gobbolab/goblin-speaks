import typer
import pygame
import board
import digitalio
import dispenser
import animatronic
from audio_player import AudioPlayer
from version import __version__

audio_player = AudioPlayer()

animatronic = animatronic.AnimatronicFactory.create()
dispenser = dispenser.DispenserFactory.create()

app = typer.Typer(help="Goblin Speaks fortune teller software")

def play():
    """
    Executes one play of the machine.
    1. Selects an audio file to play at random
    2. Activates the animatronic
    3. Dispenses card when audio complete
    """
    print("Starting play...")

    duration = audio_player.play_random()
    animatronic.animate(duration)

    print("Audio/animations complete...")
    
    dispenser.dispense()

    print("Play finished.")

def run_test_menu():
    menu_options = {
        "1": ("Play", play),
        "2": ("Test Animatronic", animatronic.test),
        "3": ("Test Dispenser", dispenser.dispense),
        "4": ("Test Audio", audio_player.play_random),
        "0": ("Exit", None)
    }

    while True:
        print("\nMenu:")
        for key, (description, _) in menu_options.items():
            print(f"{key}. {description}")

        choice = input("Enter your choice: ")

        if choice == "0":
            print("Exiting...")
            break

        selected_option = menu_options.get(choice)

        if selected_option:
            description, func = selected_option
            func() 
        else:
            print("Invalid input.")

@app.command()
def run():
    typer.echo("Run mode not implemented")

@app.command()
def test():
    run_test_menu()

if __name__ == "__main__":
    print(f"Goblin Speaks Fortune Teller Framework - {__version__}")
    app()