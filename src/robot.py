import magicbot
import wpilib
from magicbot import tunable
from robotpy_ext.control.toggle import Toggle
from wpilib.buttons import JoystickButton

from common.ctre import WPI_TalonSRX, WPI_VictorSPX
from wpilib.kinematics import DifferentialDriveKinematics
from common.rev import CANSparkMax, IdleMode, MotorType
from components import Drive, Intake
from common.camera_server import CameraServer

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

    TRACK_WIDTH = 0.43  # Units: Meters

    def createObjects(self):
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)
        self.joystick_alt = wpilib.Joystick(2)

        # Buttons
        self.btn_intake_in = JoystickButton(self.joystick_alt, 3)
        self.btn_intake_out = JoystickButton(self.joystick_alt, 5)
        self.btn_slow_movement = Toggle(self.joystick_right, 3)

        # Set up Speed Controller Groups
        self.left_motors = wpilib.SpeedControllerGroup(
            CANSparkMax(1, MotorType.kBrushless),
            CANSparkMax(2, MotorType.kBrushless),
        )

        self.right_motors = wpilib.SpeedControllerGroup(
            CANSparkMax(3, MotorType.kBrushless),
            CANSparkMax(4, MotorType.kBrushless),
        )

        # Drivetrain
        self.train = wpilib.drive.DifferentialDrive(self.left_motors, self.right_motors)

        # Intake
        self.intake_motor = WPI_VictorSPX(1)

        # Kinematics
        self.kinematics = DifferentialDriveKinematics(self.TRACK_WIDTH)  # Track width in meters


    def teleopInit(self):
        self.drive.speed_constant = 1.05
        self.drive.rotational_constant = 0.5

    def teleopPeriodic(self):
        self.drive.move(-self.joystick_left.getY(),
                        self.joystick_right.getX())

        if self.btn_slow_movement:
            # 10% of original values
            self.drive.rotational_constant = 0.05
            self.drive.speed_constant = 0.105
        else:
            self.drive.rotational_constant = 0.5
            self.drive.speed_constant = 1.05

        # Intake
        if self.btn_intake_out.get():
            self.intake.spin(1)
        elif self.btn_intake_in.get():
            self.intake.spin(-1)

        # #slow movement using POV on joystick_alt
        # if self.joystick_alt.getPOV() == 0:
        #     self.drive.move(0.2, 0)
        # elif self.joystick_alt.getPOV() == 180:
        #     self.drive.move(-0.2, 0)
        # elif self.joystick_akt.getPOV() == 90:
        #     self.drive.move(0, -0.2)
        # elif self.joystick_alt.getPOV() == 270:
        #     self.drive.move(0, 0.2)

        # print(self.joystick_alt.getPOV())


if __name__ == '__main__':
    wpilib.run(Robot)
