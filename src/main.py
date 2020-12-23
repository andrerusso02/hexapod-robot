
from legs_moves import *
import robot
import time
from math import *


all_legs_list = robot.init()
robot.start(all_legs_list)



robot.shut_down(all_legs_list)
print("fin")