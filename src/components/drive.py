import wpilib
import wpilib.drive
from wpilib.controller import PIDController
from common.navx import navx
from magicbot import will_reset_to
from networktables.util import ntproperty


class Drive:
    """
    Handle robot drivetrain.
    All drive interaction must go through this class.
    """

    train: wpilib.drive.DifferentialDrive
    y = will_reset_to(0)
    rot = will_reset_to(0)
    deadband = will_reset_ 
   def move(self, y: float, rot: float):
        """
        Move robot.
        :param y: Speed of motion in the y direction. [-1..1]
        :param rot: Speed of rotation. [-1..1]
        """
        self.y = y
        self.rot = rot

    def execute(self):
        """
        Handle driving.
        """
        self.train.setDeadband(self.deadband)