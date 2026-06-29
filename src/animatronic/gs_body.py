from .base import Animatronic
from adafruit_servokit import ServoKit
from src.config import Config
import threading
import time

class GSBody(Animatronic):
    def __init__(self, config_prefix=None):
        config = Config()
        prefix = config_prefix or 'animatronic.gs_body'

        def get_conf(key, default):
            return config.get(f'{prefix}.{key}', default)
        
        # Load servo pin configuration with defaults
        self.arm_pin   = get_conf('arm_pin', 0)
        self.mouth_pin = get_conf('mouth_pin', 1)
        
        # Load mouth animation parameters with defaults
        self.mouth_movement_delay = get_conf('mouth_movement_delay', 0.2)
        self.mouth_closed_angle   = get_conf('mouth_closed_angle', 70)
        self.mouth_open_angle     = get_conf('mouth_open_angle', 180)
        
        # Load arm animation parameters with defaults
        self.arm_start    = get_conf('arm_start', 0)
        self.arm_end      = get_conf('arm_end', 10)
        self.arm_duration = get_conf('arm_duration', 0.5)
        self.arm_steps    = get_conf('arm_steps', 200)
        self.arm_delay    = get_conf('arm_delay', 1)
        
        # Load test parameters with defaults
        self.arm_test_duration   = get_conf('arm_test_duration', 3)
        self.mouth_test_duration = get_conf('mouth_test_duration', 3)

        # --- Log Loaded Values ---
        print("Values Loaded:")
        print(f"Arm Pin: {self.arm_pin}")
        print(f"Mouth Pin: {self.mouth_pin}")
        print(f"Mouth Delay: {self.mouth_movement_delay}s")
        print(f"Mouth Angles: {self.mouth_closed_angle}° (Closed) -> {self.mouth_open_angle}° (Open)")
        print(f"Arm Angles: {self.arm_start}° (Start) -> {self.arm_end}° (End)")
        print(f"Arm Motion: {self.arm_duration}s duration, {self.arm_steps} steps, {self.arm_delay}s delay")
        print(f"Test Durations: Arm {self.arm_test_duration}s, Mouth {self.mouth_test_duration}s\n")
        
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