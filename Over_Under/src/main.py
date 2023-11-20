#region VEXcode Generated Robot Configuration
from vex import *


# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller1 = Controller(PRIMARY)
direction = "normal"
wingsenabled = False
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
d["direction"] = {}
d["direction"]["forward"] = 1
d["direction"]["backwards"] = -1
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
d["normal"] = 1
d["reversed"] = -1

class Motors:
        def __init__(self):
            self.back_left=Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
            self.front_left=Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
            self.back_right=Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
            self.front_right=Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
            self.right_puncher=Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
            self.left_puncher=Motor(Ports.PORT7, GearSetting.RATIO_36_1, True)
            self.right_wing=Motor(Ports.PORT15, GearSetting.RATIO_36_1, True)
            self.puncher_group = MotorGroup(self.right_puncher, self.left_puncher)

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

        def MotorsStop(self):
            self.front_left.stop()
            self.back_left.stop()
            self.front_right.stop()
            self.back_right.stop()

        def MotorsBrake(self):
            self.front_left.stop(BRAKE)
            self.back_left.stop(BRAKE)
            self.front_right.stop(BRAKE)
            self.back_right.stop(BRAKE)

        def MoveTo(self, forward, right, direction):
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
                    radians = 1.57079 * d[direction]
                if right > 0:
                    radians = -1.57079 * d[direction]
            else:
                radians = (math.atan(right/forward))
                if forward < 0 and right < 0:
                    radians -= math.pi * d[direction]
                if forward < 0 and right > 0:
                    radians += math.pi * d[direction]
            lengthOfArc = 4.5518 * radians          #10 inches is the diameter between wheels of the robot, 5 inches is the radius   #Changed to 4.5518 as it seems to be more accurate, possibly because the back motors are pushing it forward as well.
            Turns = lengthOfArc/12.566        #12.566 is the circumference of the wheels
            degree = Turns * 360
            self.MotorsDSpin(degree, 20, MoveToDirection)

            Turns = (length*12)/12.566          #length is multiplied by 12 so that it is defined in feet rather than inches; the 12.566 is also in inches so multiplying it by 12 cancels them into feet
            degree = Turns * 360
            self.MotorsDSpin(degree * d[direction], 100, "forward")      #The direction here should always be forward since it is facing its target

        def Turn(self, clockdirection, degrees, speed):
            ArcPercentage = degrees/360                   #Percentage of the total arc length of the robot spinning 360 degrees
            length = ArcPercentage*28.6
            degree_amount = (length/12.566)*360
            self.back_left.spin_to_position(-degree_amount * d[clockdirection], DEGREES, speed, PERCENT, False)
            self.front_left.spin_to_position(-degree_amount * d[clockdirection], DEGREES, speed, PERCENT, False)
            self.front_right.spin_to_position(degree_amount * d[clockdirection], DEGREES, speed, PERCENT, False)
            self.back_right.spin_to_position(degree_amount  * d[clockdirection], DEGREES, speed, PERCENT, True)
        
        def Drive(self):
            brain.screen.print("DriveThread")
            
            while True:
                drive_train.LeftMotorsVSpin((controller1.axis3.position()+(d[direction]*(controller1.axis1.position() * .7)/(1+abs(controller1.axis3.position()/100))))*d[direction])
                drive_train.RightMotorsVSpin((controller1.axis3.position()-(d[direction]*(controller1.axis1.position() * .7)/(1+abs(controller1.axis3.position()/100))))*d[direction])
                if abs(controller1.axis3.position()) < 1 and abs(controller1.axis1.position()) < 1:
                    self.MotorsBrake()
                wait(5, MSEC)

        def ChangeDriveDirection(self):
            global direction
            if direction == "normal":
                direction = "reversed"
            else:
                direction = "normal"

        def PositionPuncher(self):
            brain.screen.print("Line 127")
            self.puncher_group.set_max_torque(2, PERCENT)
            self.puncher_group.spin(FORWARD, 100, PERCENT)             #Change this to run until the motor experiences a ton of torque
            wait(.3, SECONDS)
            self.puncher_group.stop(COAST)
            wait(.2, SECONDS)
            self.puncher_group.set_max_torque(100, PERCENT)

        def PrimePuncher(self):
            brain.screen.print("line 134")
            self.puncher_group.set_position(0, DEGREES)
            self.puncher_group.spin_to_position(250, DEGREES, 100, PERCENT, True)

        def LaunchPuncher(self):
            self.puncher_group.set_position(0, DEGREES)
            self.puncher_group.spin_to_position(-60, DEGREES, 100, PERCENT)
        
        def UnprimeCatapult(self):
            self.puncher_group.set_position(0, DEGREES)
            self.puncher_group.spin_to_position(-250, DEGREES, 100, PERCENT)
        
        def PuncherNotPrimed(self):
            brain.screen.print("line150")
            while True:
                if controller1.buttonA.pressing() == True:
                    brain.screen.print("Line 152")
                    self.PrimePuncher()
                    self.PrimedThread = Thread(self.PuncherIsPrimed())
                    game.NotPrimedThread.stop()
                wait(5, MSEC)
            
        def PuncherIsPrimed(self):
            brain.screen.clear_screen()
            brain.screen.print("CatapultIsPrimed Thread IS On")
            while True:
                if controller1.buttonA.pressing() == True:
                    self.UnprimeCatapult()
                    self.NotPrimedThread = Thread(drive_train.PuncherNotPrimed())
                    self.PrimedThread.stop()
                if controller1.buttonB.pressing() == True:
                    self.LaunchPuncher()
                    self.PrimePuncher()
                wait(5, MSEC)

        def Puncher(self):
            while True:
                if controller1.buttonA.pressing() == True:
                    self.puncher_group.set_position(0, DEGREES)
                    self.puncher_group.spin_to_position(360, DEGREES, 100, PERCENT, True)

        def SpinPuncher(self):
            self.puncher_group.set_position(0, DEGREES)
            self.puncher_group.spin_to_position(360, DEGREES, 100, PERCENT, True)

        def Wings(self):
            self.right_wing.set_position(0, DEGREES)
            controller1.buttonUp.pressed(self.EnableWings)
            controller1.buttonDown.pressed(self.DisableWings)
        
        def EnableWings(self):
            global wingsenabled
            wingsenabled = True
            self.right_wing.spin_to_position(-90, DEGREES, 100, PERCENT, True)
            while wingsenabled == True:
                self.right_wing.stop(BRAKE)
                brain.screen.print("TRUEEEEE")
                if abs(abs(self.right_wing.position()) - 90) > 5:
                    self.right_wing.spin_to_position(-90, DEGREES)

        def DisableWings(self):
            global wingsenabled
            wingsenabled = False
            self.right_wing.spin_to_position(0, DEGREES, 100, PERCENT, True)
            while wingsenabled == False:
                self.right_wing.stop(BRAKE)
                brain.screen.print("FALLSEE")
                if abs(self.right_wing.position()) > 5:
                    self.right_wing.spin_to_position(0, DEGREES)
            

class Game():
        def driverControl(self):
            brain.screen.print("line 169")
            self.NotPrimedThread = Thread(drive_train.Puncher)
            self.DrivingThread = Thread(drive_train.Drive)
            #self.WingsThread = Thread(drive_train.Wings)
            controller1.buttonL2.pressed(drive_train.ChangeDriveDirection)
        def autonomous(self):
            #drive_train.SpinPuncher()
            drive_train.LeftMotorsVSpin(100)
            drive_train.RightMotorsVSpin(100)
            wait(2, SECONDS)
            drive_train.LeftMotorsVSpin(-100)
            drive_train.RightMotorsVSpin(-100)
            wait(.5, SECONDS)
            drive_train.MotorsBrake()
            #drive_train.Turn("clockwise", 30, 100)
            #drive_train.MoveTo(3.92, 0, "normal")



drive_train = Motors()
game = Game()



#Main
competition = Competition(game.driverControl, game.autonomous)

