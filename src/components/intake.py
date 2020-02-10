import wpilib
from wpilib.interfaces import SpeedController
from wpilib import VictorSP
from magicbot import will_reset_to

class Intake:
    intake_motor: VictorSP

    speed = will_reset_to(0)

    def spin(self, speed: float):
        self.speed = speed

    def execute(self):
        self.intake_motor.set(self.speed)
