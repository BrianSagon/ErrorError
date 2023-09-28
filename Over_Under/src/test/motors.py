from vex import *

class Motors:
    def __init__(self):
        self.back_left=Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
        self.front_left=Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
        self.back_right=Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
        self.front_right=Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)

    def drive(self, t):
        self.back_left.spin_for(DirectionType.FORWARD, 2, TimeUnits.SECONDS)
        self.front_left.spin_for(DirectionType.FORWARD, 2, TimeUnits.SECONDS)
        self.back_right.spin_for(DirectionType.FORWARD, 2, TimeUnits.SECONDS)
        self.front_right.spin_for(DirectionType.FORWARD, 2, TimeUnits.SECONDS)

