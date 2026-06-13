from .base import Animatronic
from adafruit_servokit import ServoKit
import threading

mouth_movement_delay = 0.2
mouth_closed_angle = 70
mouth_open_angle = 180

arm_start = 0
arm_end = 10
arm_duration = 0.5
arm_steps = 200
arm_delay = 1

class GSBody(Animatronic):
    def __init__(self, arm_pin, mouth_pin, *args, **kwargs):
        """
        Initializes the GSBody with arm and mouth servo pins.
        """
        kit = ServoKit(channels=16)

        self.arm = kit.servo[arm_pin]
        self.mouth = kit.servo[mouth_pin]
        

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
        Runs a quick diagnostic sweep of the servos.
        """
        print("Testing arm and mouth servos...")
        return True

    def __animate_mouth(self, duration):
        print("Starting mouth animation...")
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            self.mouth.angle = mouth_open_angle
            time.sleep(mouth_movement_delay)
            self.mouth.angle = mouth_closed_angle
            time.sleep(mouth_movement_delay)

    def __animate_arm(self, duration):
        print("Starting arm animation...")
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            self.__smooth_servo_movement(self.arm, arm_start, arm_end, arm_duration, arm_steps)
            time.sleep(1)
            self.__smooth_servo_movement(self.arm, arm_end, arm_start, arm_duration, arm_steps)
            time.sleep(1)

    def __smooth_servo_movement(self, servo, start_angle, end_angle, duration, steps=50):
        angle_increment = (end_angle - start_angle) / steps
        time_per_step = duration / steps
        
        for i in range(steps + 1):
            servo.angle = start_angle + (angle_increment * i)
            time.sleep(time_per_step)