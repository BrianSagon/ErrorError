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
                
        
        def MotorsDSpin(self, degree_amount, speed, direction):
            self.front_right.set_position(0, DEGREES)
            self.back_right.set_position(0, DEGREES)
            self.front_left.set_position(0, DEGREES)
            self.back_left.set_position(0, DEGREES)
            self.back_left.spin_to_position(degree_amount, DEGREES, speed, PERCENT, False)
            self.front_left.spin_to_position(degree_amount, DEGREES, speed, PERCENT, False)
            self.front_right.spin_to_position(degree_amount, DEGREES, speed, PERCENT, False)
            self.back_right.spin_to_position(degree_amount, DEGREES, speed, PERCENT, True)      #True since it is the last one to be called, activating it and the other spin_to's next that have been activated
            

        def MoveTo(self, forward, right):
            if forward > 0 and right > 0:
                length = math.sqrt((forward ** 2) + (right ** 2))
                radians = math.atan(right/forward)
                lengthOfArc = 5 * radians          #10 inches is the distance between wheels of the robot, 5 inches is the radius
                Turns = lengthOfArc/12.566        #12.566 is the circumference of the wheels
                degree = Turns * 360
                self.LeftMotorsDSpin(degree, 20)
                self.RightMotorsDSpin(-degree, 20)
                Turns = (length*12)/12.566          #length is multiplied by 12 so that it is defined in feet rather than inches
                degree = Turns * 360
                self.LeftMotorsDSpin(degree, 100)
                self.RightMotorsDSpin(degree, 100)
                

drive_train = Motors()



while True:
    drive_train.LeftMotorsVSpin(controller1.axis3.position()+(controller1.axis4.position()/2))
    drive_train.RightMotorsVSpin(controller1.axis3.position()-(controller1.axis4.position()/2))