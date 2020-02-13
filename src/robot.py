import magicbot
import wpilib
from wpilib import VictorSP
from magicbot import tunable
from robotpy_ext.control.toggle import Toggle
from wpilib.buttons import JoystickButton

from common.ctre import WPI_TalonSRX, WPI_VictorSPX
from wpilib.kinematics import DifferentialDriveKinematics
from common.rev import IdleMode, MotorType
from components import Drive, Intake

r"""
/ \                / \
\ /       (+)      \ /
           |
           |X
(+) -------|--Y----  (-)
           |
           |
/ \       (-)      / \
\ /                \ /

Counter-Clockwise is Positive
   /-\ ^
   |X| | (+)
   \-/ |
   -->
"""


class Robot(magicbot.MagicRobot):
    drive: Drive
    intake: Intake

    def createObjects(self):
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)
        self.joystick_alt = wpilib.Joystick(2)

        # Buttons
        self.btn_intake_in = JoystickButton(self.joystick_alt, 2)
        self.btn_intake_out = JoystickButton(self.joystick_alt, 1)

        # Set up Speed Controller Groups
        self.left_motors = wpilib.SpeedControllerGroup(
            VictorSP(0),
            VictorSP(1),
        )

        self.right_motors = wpilib.SpeedControllerGroup(
            VictorSP(2),
            VictorSP(3),
        )

        # Drivetrain
        self.train = wpilib.drive.DifferentialDrive(self.left_motors, self.right_motors)

        # Intake
        self.intake_motor = VictorSP(4)

    def teleopPeriodic(self):
        self.drive.move(-self.joystick_left.getY(),
                        self.joystick_right.getX())

        # Intake
        if self.btn_intake_out.get():
            if self.joystick_right.getX() >= -0.1 and self.joystick_right.getX() <= 0.1:
                self.intake.spin(1)
        elif self.btn_intake_in.get():
            self.intake.spin(-1)

if __name__ == '__main__':
    wpilib.run(Robot)
