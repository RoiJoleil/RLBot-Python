import math
from objects import *

#Finds out the required acceleration to reach a target.
def acceleration(target, car, time, gravity = 650):
    velocity_required = (target - car.location) / time
    acceleration_required = velocity_required - car.velocity
    acceleration_required[2] += (gravity * time)
    return acceleration_required
