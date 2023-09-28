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

# Begin project code

class Motors:
        def __init__(self):
            self.back_left=Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
            self.front_left=Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
            self.back_right=Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
            self.front_right=Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)

        def LeftMotorsSpin(self, velocity):
            self.back_left.spin(FORWARD, velocity, PERCENT)
            self.front_left.spin(FORWARD, velocity, PERCENT)

        def RightMotorsSpin(self, velocity):
            self.front_right.spin(FORWARD, velocity, PERCENT)
            self.back_right.spin(FORWARD, velocity, PERCENT)
        
drive_train = Motors()

while True:
    drive_train.LeftMotorsSpin(controller1.axis3.position()+(controller1.axis1.position()/(1+abs(controller1.axis3.position()/100))))
    drive_train.RightMotorsSpin(controller1.axis3.position()-(controller1.axis1.position()/(1+abs(controller1.axis3.position()/100))))