from .base import Animatronic
from adafruit_servokit import ServoKit
from src.config import Config
import threading
import time

class GSBody(Animatronic):
    def __init__(self, *args, **kwargs):
        """
        Initializes the GSBody with configuration from goblin-speaks-config.yml
        """
        config = Config()
        
        # Load servo pin configuration with defaults
        self.arm_pin = config.get('animatronic.gs_body.arm_pin', 0)
        self.mouth_pin = config.get('animatronic.gs_body.mouth_pin', 1)
        
        # Load mouth animation parameters with defaults
        self.mouth_movement_delay = config.get('animatronic.gs_body.mouth_movement_delay', 0.2)
        self.mouth_closed_angle = config.get('animatronic.gs_body.mouth_closed_angle', 70)
        self.mouth_open_angle = config.get('animatronic.gs_body.mouth_open_angle', 180)
        
        # Load arm animation parameters with defaults
        self.arm_start = config.get('animatronic.gs_body.arm_start', 0)
        self.arm_end = config.get('animatronic.gs_body.arm_end', 10)
        self.arm_duration = config.get('animatronic.gs_body.arm_duration', 0.5)
        self.arm_steps = config.get('animatronic.gs_body.arm_steps', 200)
        self.arm_delay = config.get('animatronic.gs_body.arm_delay', 1)
        
        # Load test parameters with defaults
        self.arm_test_duration = config.get('animatronic.gs_body.arm_test_duration', 3)
        self.mouth_test_duration = config.get('animatronic.gs_body.mouth_test_duration', 3)
        
        kit = ServoKit(channels=16)
        self.arm = kit.servo[self.arm_pin]
        self.mouth = kit.servo[self.mouth_pin]

    def animate(self, duration: float):
        """
        Performs animation logic over the specified duration.
        """
        print(f"Animating GS body for {duration} seconds...")

        talk_thread = threading.Thread(
            target=self.__animate_mouth, 
            args=(duration,), 
            daemon=True
        )

        arm_thread = threading.Thread(
            target=self.__animate_arm,
            args=(duration,),
            daemon=True
        )
        
        talk_thread.start()
        arm_thread.start()
            
        talk_thread.join()
        arm_thread.join()
        
        print("Animation complete!")

    def test(self):
        """
        Runs a quick diagnostic sweep of animatronic.
        """
        print(f"Testing arm (for {self.arm_test_duration}s) and mouth (for {self.mouth_test_duration}s) servos...")
        self.__animate_arm(self.arm_test_duration)
        self.__animate_mouth(self.mouth_test_duration)

    def __animate_mouth(self, duration):
        print("Starting mouth animation...")
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            self.mouth.angle = self.mouth_open_angle
            time.sleep(self.mouth_movement_delay)
            self.mouth.angle = self.mouth_closed_angle
            time.sleep(self.mouth_movement_delay)

    def __animate_arm(self, duration):
        print("Starting arm animation...")
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            self.__smooth_servo_movement(self.arm, self.arm_start, self.arm_end, self.arm_duration, self.arm_steps)
            time.sleep(self.arm_delay)
            self.__smooth_servo_movement(self.arm, self.arm_end, self.arm_start, self.arm_duration, self.arm_steps)
            time.sleep(self.arm_delay)

    def __smooth_servo_movement(self, servo, start_angle, end_angle, duration, steps=50):
        angle_increment = (end_angle - start_angle) / steps
        time_per_step = duration / steps
        
        for i in range(steps + 1):
            servo.angle = start_angle + (angle_increment * i)
            time.sleep(time_per_step)