from adafruit_servokit import ServoKit
import typer
import threading
import time
import pygame
import board
import digitalio
import dispenser
from audio_player import AudioPlayer

audio_player = AudioPlayer()

kit = ServoKit(channels=16)

mouth = kit.servo[0]
mouth_movement_delay = 0.2
mouth_closed_angle = 70
mouth_open_angle = 180

arm = kit.servo[1]
arm_start = 0
arm_end = 10
arm_duration = 0.5
arm_steps = 200
arm_delay = 1

card = dispenser.GSCardDispenser(board.D17, board.D18, board.D19, board.D20)

app = typer.Typer(help="Goblin Speaks fortune teller software")

def smooth_servo_movement(servo, start_angle, end_angle, duration, steps=50):
    """
    Moves servo smoothishly from a start angle to an end angle over a specified duration.
    """
    angle_increment = (end_angle - start_angle) / steps
    time_per_step = duration / steps
    
    for i in range(steps + 1):
        servo.angle = start_angle + (angle_increment * i)
        time.sleep(time_per_step)

def talk_animation(duration):
    """
    Runs the jaw animation open/close loop for a specific duration in seconds.
    """
    print("Starting mouth animation...")

    start_time = time.time()
    
    while (time.time() - start_time) < duration:
        mouth.angle = mouth_open_angle
        time.sleep(mouth_movement_delay)
        
        mouth.angle = mouth_closed_angle
        time.sleep(mouth_movement_delay)

def arm_animation(druation):
    """
    Runs the arm animation loop for a specific duration in seconds.
    """
    print("Starting arm animation...")

    while (time.time() - start_time) < duration:
        smooth_servo_movement(arm, arm_start, arm_end, arm_duration, arm_steps)
        time.sleep(1)
        smooth_servo_movement(arm, arm_end, arm_start, arm_duration, arm_steps)
        time.sleep(1)

def play():
    """
    Executes one play of the machine.
    1. Selects an audio file to play at random
    2. Activates the animatronic
    3. Dispenses card when audio complete
    """
    print("Starting play...")

    duration = audio_player.playrandom()
    
    talk_thread = threading.Thread(
        target=talk_animation, 
        args=(duration,), 
        daemon=True
    )
    talk_thread.start()

    arm_thread = threading.Thread(
        target=arm_animation,
        args=(duration,),
        daemon=True
    )
    arm_thread.start()
        
    talk_thread.join()
    arm_thread.join()

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
    app()