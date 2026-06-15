# source env/bin/activate
# kick buil

from adafruit_servokit import ServoKit
from stepper import Stepper
import threading
import time
import pygame
import board
import digitalio

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

card = Stepper(board.D17, board.D18, board.D27, board.D22)

coin_beam = digitalio.DigitalInOut(board.D21)
coin_beam.direction = digitalio.Direction.INPUT
coin_beam.pull = digitalio.Pull.UP
should_accept_coin = True

is_talking = False

play_delay = 1

pygame.mixer.init()

def talk_animation():
    while True:
        if is_talking:
            mouth.angle = mouth_open_angle
            time.sleep(mouth_movement_delay)
            mouth.angle = mouth_closed_angle
            time.sleep(mouth_movement_delay)
        else:
            time.sleep(0.1)

def arm_animation():
    while True:
        if is_talking:
            smooth_servo_movement(arm, arm_start, arm_end, arm_duration, arm_steps)
            time.sleep(1)
            smooth_servo_movement(arm, arm_end, arm_start, arm_duration, arm_steps)
            time.sleep(1)
        else:
            time.sleep(0.1)

def detect_coin():
    global should_accept_coin
    while True:
        if not coin_beam.value and should_accept_coin:
            print('\nCoin detected, starting play...')
            play()
        if should_accept_coin:
            time.sleep(0.05)
        else:
            time.sleep(0.1)

def play_voice():
    global is_talking
    pygame.mixer.music.load("zoltar.mp3")
    is_talking = True
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    is_talking = False
    print("Audio complete.")

def dispense_card():
    card.move_backward(3000)

def play():
    global should_accept_coin

    should_accept_coin = False

    print("Starting play...")
    time.sleep(play_delay)

    print("Starting audio...")
    play_voice()
        
    print("Dispensing card...")
    dispense_card()

    should_accept_coin = True
    print("Play finished.")

def process_input():
    while True:
        print("\nMenu:")
        print("1. Play")
        print("2. Test Card")
        print("3. Test Voice")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            play()
        elif choice == "2":
            print("Testing card dispenser...")
            dispense_card()
        elif choice == "3":
            print("Testing voice...")
            play_voice()
        elif choice == "0":
            print("Exiting...")
            return
        else:
            print("Invalid input.")

def smooth_servo_movement(servo, start_angle, end_angle, duration, steps=50):
    angle_increment = (end_angle - start_angle) / steps
    time_per_step = duration / steps
    
    for i in range(steps + 1):
        servo.angle = start_angle + (angle_increment * i)
        time.sleep(time_per_step)

def main():
    print("Welcome to Goblin Speaks!")
    mouth.angle = mouth_closed_angle
    
    print("Starting talking thread...")
    talk_thread = threading.Thread(target=talk_animation, daemon=True)
    talk_thread.start()

    print("Starting arm thread...")
    arm_thread = threading.Thread(target=arm_animation, daemon=True)
    arm_thread.start()

    print("Starting coin detection thread...")
    # coin_thread = threading.Thread(target=detect_coin, daemon=True)
    # coin_thread.start()

    print("Startup complete. Ready to process input.")
    process_input()

if __name__ == "__main__":
    main()
