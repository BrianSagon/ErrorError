#region VEXcode Generated Robot Configuration
from vex import *


# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller1 = Controller(PRIMARY)


# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
import math

# Begin project code

class Motors:
        def __init__(self):
            self.back_left=Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
            self.front_left=Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
            self.back_right=Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
            self.front_right=Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)

        def LeftMotorsVSpin(self, velocity):
            self.back_left.spin(FORWARD, velocity, PERCENT)
            self.front_left.spin(FORWARD, velocity, PERCENT)

        def RightMotorsVSpin(self, velocity):
            self.front_right.spin(FORWARD, velocity, PERCENT)
            self.back_right.spin(FORWARD, velocity, PERCENT)
        
        def RightMotorsDSpin(self, degree_amount):
            self.front_right.spin_to_position(degree_amount, DEGREES)
            self.back_right.spin_to_position(degree_amount, DEGREES)

        def LeftMotorsDSpin(self, degree_amount):
            self.back_left.spin(degree_amount, DEGREES)
            self.front_left.spin(degree_amount, DEGREES)

        def MoveTo(self, forward, right):
            if forward > 0 and right > 0:
                length = math.sqrt((forward ** 2) + (right ** 2))
                degree = math.atan(right/forward)
                self.LeftMotorsDSpin(degree)
                self.RightMotorsDSpin(-degree)
                

drive_train = Motors()


drive_train.LeftMotorsDSpin(50)


while True:
    drive_train.LeftMotorsVSpin(controller1.axis3.position()+(controller1.axis4.position()/2))
    drive_train.RightMotorsVSpin(controller1.axis3.position()-(controller1.axis4.position()/2))