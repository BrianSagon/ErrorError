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

d = {}
d["forward"] = {}
d["forward"]["right"] = 1
d["forward"]["left"] = 1
d["back"] = {}
d["back"]["right"] = 1
d["back"]["left"] = 1
d["right"] = {}
d["right"]["right"] = -1
d["right"]["left"] = 1
d["left"] = {}
d["left"]["right"] = -1
d["left"]["left"] = 1
d["still"] = {}
d["still"]["right"] = 0
d["still"]["left"] = 0
d["clockwise"] = -1
d["counterclockwise"] = 1
class Motors:
        def __init__(self):
            self.back_left=Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
            self.front_left=Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
            self.back_right=Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
            self.front_right=Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
            self.catapult=Motor(Ports.PORT4,GearSetting.RATIO_36_1, True)

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
            self.back_left.spin_to_position(degree_amount * d[direction]["left"], DEGREES, speed, PERCENT, False)
            self.front_left.spin_to_position(degree_amount * d[direction]["left"], DEGREES, speed, PERCENT, False)
            self.front_right.spin_to_position(degree_amount * d[direction]["right"], DEGREES, speed, PERCENT, False)
            self.back_right.spin_to_position(degree_amount  * d[direction]["right"], DEGREES, speed, PERCENT, True)    #True since it is the last one to be called, activating it and the other spin_to's next that have been activated

        def MoveTo(self, forward, right):
            MoveToDirection = "still"
            if right == 0:
                if forward > 0:
                    MoveToDirection = "forward"
                elif forward < 0:
                    MoveToDirection = "back"
            elif right < 0:
                MoveToDirection = "left"
            elif right > 0:
                MoveToDirection = "right"

            length = math.sqrt((forward ** 2) + (right ** 2))
    
            radians = 0
            if forward == 0:                 #I'm not adding a check for if both are zero, as that should never happen
                if right < 0:                  #this is all the calculation for the amount of radians that the robot needs to turn
                    radians = 1.57079
                if right > 0:
                    radians = -1.57079
            else:
                radians = (math.atan(right/forward))
                if forward < 0 and right < 0:
                    radians -= math.pi
                if forward < 0 and right > 0:
                    radians += math.pi
            lengthOfArc = 4.5518 * radians          #10 inches is the diameter between wheels of the robot, 5 inches is the radius   #Changed to 4.5518 as it seems to be more accurate, possibly because the back motors are pushing it forward as well.
            Turns = lengthOfArc/12.566        #12.566 is the circumference of the wheels
            degree = Turns * 360
            self.MotorsDSpin(degree, 20, MoveToDirection)

            Turns = (length*12)/12.566          #length is multiplied by 12 so that it is defined in feet rather than inches; the 12.566 is also in inches so multiplying it by 12 cancels them into feet
            degree = Turns * 360
            self.MotorsDSpin(degree, 100, "forward")      #The direction here should always be forward since it is facing its target

        def Turn(self, clockdirection, degrees, speed):
            ArcPercentage = degrees/360                   #Percentage of the total arc length of the robot spinning 360 degrees
            length = ArcPercentage*28.6
            degree_amount = (length/12.566)*360
            self.back_left.spin_to_position(-degree_amount * d[clockdirection], DEGREES, speed, PERCENT, False)
            self.front_left.spin_to_position(-degree_amount * d[clockdirection], DEGREES, speed, PERCENT, False)
            self.front_right.spin_to_position(degree_amount * d[clockdirection], DEGREES, speed, PERCENT, False)
            self.back_right.spin_to_position(degree_amount  * d[clockdirection], DEGREES, speed, PERCENT, True)
        
        def Drive(self):
            while True:
                drive_train.LeftMotorsVSpin(controller1.axis3.position()+(controller1.axis1.position()/(1+abs(controller1.axis3.position()/100))))
                drive_train.RightMotorsVSpin(controller1.axis3.position()-(controller1.axis1.position()/(1+abs(controller1.axis3.position()/100))))
                sleep(5)

        def PositionCatapult(self, velocity):
            brain.screen.print("Line 125")
            self.catapult.set_max_torque(4, PERCENT)
            self.catapult.spin(FORWARD, velocity, PERCENT)             #Change this to run until the motor experiences a ton of torque
            wait(.4, SECONDS)
            self.catapult.stop(COAST)
            wait(.2, SECONDS)
            self.catapult.set_max_torque(100, PERCENT)

        def PrimeCatapult(self):
            brain.screen.print("line 134")
            self.catapult.set_position(0, DEGREES)
            self.catapult.spin_to_position(180, DEGREES, 100, PERCENT, True)
            controller1.buttonB.pressed(self.LaunchCatapult)

        def LaunchCatapult(self):
            self.catapult.set_position(0, DEGREES)
            self.catapult.spin_to_position(60, DEGREES, 100, PERCENT)
        
        def UnprimeCatapult(self):
            self.catapult.set_position(0, DEGREES)
            self.catapult.spin_to_position(-160, DEGREES, 100, PERCENT)
            self.PositionCatapult
        
        def CatapultNotPrimed(self):
            wait(.2, SECONDS)
            while True:
                if controller1.buttonA.pressing() == True:
                    brain.screen.print("Line 152")
                    self.PrimeCatapult()
                    #wait(.2, SECONDS)
                    Thread(self.CatapultIsPrimed)
                    break
                sleep(10)
            
        def CatapultIsPrimed(self):
            wait(.2, SECONDS)
            brain.screen.clear_screen()
            brain.screen.print("CatapultIsPrimed Thread IS On")
            while True:
                if controller1.buttonA.pressing() == True:
                    self.UnprimeCatapult()
                    Thread(self.CatapultNotPrimed)
                    break
                if controller1.buttonB.pressing() == True:
                    self.LaunchCatapult()
                    self.PositionCatapult(100)
                    self.PrimeCatapult()
                sleep(10)

                
        
        
            
                
                

drive_train = Motors()



#Main
def 
drive_train.PositionCatapult(100)
Thread(drive_train.Drive)
Thread(drive_train.CatapultNotPrimed)

    
