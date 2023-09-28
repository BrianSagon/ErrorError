from enum import Enum
from collections import namedtuple

Direction = namedtuple('Direction', ['right_direction', 'left_direction'])

class Directions(Enum):

    @property
    def right_direction(self):
        self.value.right_direction

    @property
    def left_direction(self):
        self.value.left_direction

    forward = Direction(1, 1)
    left = Direction(1, -1)
    right = Direction(-1, 1)
    back = Direction(-1, -1)

print( Directions.forward.value.left_direction )
