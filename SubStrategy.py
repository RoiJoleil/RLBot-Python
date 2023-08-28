from tools import *
from routines import *
from utils import *
from Information import *
from PlayerIntention import *


#This File consists of SubStrategy for AriyaGyhraeluna.py

class gotonet():
    # Drives towards a designated (stationary) target
    # Optional vector controls where the car should be pointing upon reaching the target
    # TODO - slow down if target is inside our turn radius
    def __init__(self, target, vector=None, direction=1):
        self.target = target
        self.vector = vector
        self.direction = direction

    def run(self, agent):
        #agent.pop() Conditions

        #Getting the information using "detect_boost" function
        take_closest_boost_within_60deg, closest_boost = detect_boost(agent)

        targets = {"goal" : (agent.foe_goal.left_post, agent.foe_goal.right_post), "anywhere_but_our_net": (agent.friend_goal.right_post, agent.friend_goal.left_post)}
        shots = find_hits(agent, targets)
        is_teammate_going_result = is_teammate_going(agent)
        if len(shots["goal"]) > 0 and is_teammate_going_result is False:
            agent.pop()
            agent.push(shots["goal"][0])

        if take_closest_boost_within_60deg and not agent.me.boost > 20:
            agent.pop()
            agent.push(goto_boost(closest_boost, agent.ball.location))

        if len(shots["anywhere_but_our_net"]) > 0 and is_teammate_going_result is False:
            agent.push(shots["anywhere_but_our_net"][0])

        car_to_target = self.target - agent.me.location
        distance_remaining = car_to_target.flatten().magnitude()

        agent.line(self.target - Vector3(0, 0, 500), self.target + Vector3(0, 0, 500), [255, 0, 255])

        if self.vector != None:
            # See commends for adjustment in jump_shot or aerial for explanation
            side_of_vector = sign(self.vector.cross((0, 0, 1)).dot(car_to_target))
            car_to_target_perp = car_to_target.cross((0, 0, side_of_vector)).normalize()
            adjustment = car_to_target.angle(self.vector) * distance_remaining / 3.14
            final_target = self.target + (car_to_target_perp * adjustment)
        else:
            final_target = self.target

        # Some adjustment to the final target to ensure it's inside the field and we don't try to drive through any goalposts to reach it
        if abs(agent.me.location[1]) > 5150: final_target[0] = cap(final_target[0], -750, 750)

        local_target = agent.me.local(final_target - agent.me.location)

        angles = defaultPD(agent, local_target, self.direction)
        defaultThrottle(agent, 2300, self.direction)

        agent.controller.boost = False
        agent.controller.handbrake = True if abs(angles[1]) > 2.3 else agent.controller.handbrake

        velocity = 1 + agent.me.velocity.magnitude()
        if distance_remaining < 350:
            agent.pop()
        elif abs(angles[1]) < 0.05 and velocity > 600 and velocity < 2150 and distance_remaining / velocity > 2.0:
            agent.push(flip(local_target))
        elif abs(angles[1]) > 2.8 and velocity < 200:
            agent.push(flip(local_target, True))
        elif agent.me.airborne:
            agent.push(recovery(self.target))

class gotoposition():
    def __init__(self, target, time, direction, vector=None):
        self.target = target #where we are trying to get to
        self.time = time #how fast we want to get there
        self.vector = vector #where we want to point our nose
        self.direction = direction #the direction we want to face upon reaching the destination

    def calculate_acceleration(self, agent):
        gravity = 650
        velocity_required = (self.target - agent.me.location) / self.time
        acceleration_required = velocity_required - agent.me.velocity
        acceleration_required[2] += (gravity * self.time)
        return acceleration_required

