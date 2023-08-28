import math
from tools import *
from utils import *

def me_information(agent):
    ball_to_me = agent.me.location - agent.ball.location
    ball_to_me_normalized = ball_to_me.normalize()
    me_to_ball = agent.ball.location - agent.me.location
    me_to_ball_normalized = me_to_ball.normalize()

#Returns Distance to Ball
    ball_distance_to_me = ball_to_me.magnitude()
#Returns Velocity of the Ball towards me (negative means towards)
    ball_velocity_towards_me = agent.ball.velocity.dot(me_to_ball_normalized)
#Returns Velocity of me towards the Ball (negative means towards)
    me_velocity_towards_ball = agent.me.velocity.dot(ball_to_me_normalized)

    car_me_forward = agent.me.forward
    ball_to_car_me = agent.ball.location - agent.me.location
    normalized_ball_to_car_me = ball_to_car_me.normalize()
    # Calculate the angle between the car's forward vector and the ball-to-car vector
    angle = math.degrees(math.acos(car_me_forward.dot(normalized_ball_to_car_me)))
    angle_threshold = 55
#Returns if the Ball is within an angle of me
    ball_in_front_of_me = angle <= angle_threshold

    me_info = {
        "ball_distance_to_me": ball_distance_to_me,
        "ball_velocity_towards_me": ball_velocity_towards_me,
        "me_velocity_towards_ball": me_velocity_towards_ball,
        "ball_in_front_of_me": ball_in_front_of_me
    }

    return me_info

def friend_information(agent):
    if len(agent.friends) > 0:
        friend_info = []

        for friend in agent.friends:
            ball_to_friend = friend.location - agent.ball.location
            ball_to_friend_normalized = ball_to_friend.normalize()
            friend_to_ball = agent.ball.location - friend.location
            friend_to_ball_normalized = friend_to_ball.normalize()

        #Returns Friend Distance to Ball
            ball_distance_to_friend = ball_to_friend.magnitude()
        #Returns Velocity of the Ball towards friend
            ball_velocity_towards_friend = agent.ball.velocity.dot(friend_to_ball_normalized)
        #Returns Velocity of friend towards the Ball
            friend_velocity_towards_ball = friend.velocity.dot(ball_to_friend_normalized)

            car_friend_forward = friend.forward
            ball_to_car_friend = agent.ball.location - friend.location
            normalized_ball_to_car_friend = ball_to_car_friend.normalize()
            # Calculate the angle between the car's forward vector and the ball-to-car vector
            angle = math.degrees(math.acos(car_friend_forward.dot(normalized_ball_to_car_friend)))
            angle_threshold = 55
        #Returns if the Ball is within an angle of the friend
            ball_in_front_of_friend = angle <= angle_threshold

            friend_info.append({
                "ball_distance_to_friend": ball_distance_to_friend,
                "ball_velocity_towards_friend": ball_velocity_towards_friend,
                "friend_velocity_towards_ball": friend_velocity_towards_ball,
                "ball_in_front_of_friend": ball_in_front_of_friend
            })

        return friend_info
    else:
        return []

def is_teammate_going(agent):
    if len(agent.friends) > 0:
        #imports required information
        me_infos = me_information(agent)
        friend_infos = friend_information(agent)

        #This section normalizes all the friend.infos to a value between 0 and 1
        min_distance = 250
        max_distance = 9500
        normalized_distances_friends = []
        for friend_info in friend_infos:
            ball_distance_to_friend = friend_info["ball_distance_to_friend"]
            normalized_distance_friend = max(0, min(1, 1 - (ball_distance_to_friend - min_distance) / (max_distance - min_distance)))
            normalized_distances_friends.append(normalized_distance_friend)

        min_velocity_car_friend = 2200
        max_velocity_car_friend = -2200
        normalized_velocitys_friends = []
        for friend_info in friend_infos:
            friend_velocity_towards_ball = friend_info["friend_velocity_towards_ball"]
            normalized_velocity_friend = max(0, min(1, (friend_velocity_towards_ball - min_velocity_car_friend) / (max_velocity_car_friend - min_velocity_car_friend)))
            normalized_velocitys_friends.append(normalized_velocity_friend)

        min_velocity_ball_friend = 1800
        max_velocity_ball_friend = -1800
        normalized_velocitys_ball_friends = []
        for friend_info in friend_infos:
            ball_velocity_towards_friend = friend_info["ball_velocity_towards_friend"]
            normalized_velocity_ball_friend = max(-1, min(1, (ball_velocity_towards_friend - min_velocity_ball_friend) / (max_velocity_ball_friend - min_velocity_ball_friend)))
            normalized_velocitys_ball_friends.append(normalized_velocity_ball_friend)

        for friend_info in friend_infos:
            ball_in_front_of_friend = friend_info["ball_in_front_of_friend"]
            if ball_in_front_of_friend is True:
                facing_factor_friend = 1
            else:
                facing_factor_friend = 0

        #This section normalizes all the me.infos to a value between 0 and 1
        min_distance = 250
        max_distance = 9500
        ball_distance_to_me = me_infos["ball_distance_to_me"]
        normalized_distance_me = max(0, min(1, 1 - (ball_distance_to_me - min_distance) / (max_distance - min_distance)))

        me_velocity_towards_ball = me_infos["me_velocity_towards_ball"]
        min_velocity_car_me = 2200
        max_velocity_car_me = -2200
        normalized_velocity_me = max(0, min(1, (me_velocity_towards_ball - min_velocity_car_me) / (max_velocity_car_me - min_velocity_car_me)))

        ball_velocity_towards_me = me_infos["ball_velocity_towards_me"]
        min_velocity_ball_me = 1800
        max_velocity_ball_me = -1800
        normalized_velocity_ball_me = max(-1, min(1, (ball_velocity_towards_me - min_velocity_ball_me) / (max_velocity_ball_me - min_velocity_ball_me)))

        ball_in_front_of_me = me_infos["ball_in_front_of_me"]
        if ball_in_front_of_me is True:
            facing_factor_me = 1
        else:
            facing_factor_me = 0

        #Sets the weighs to how important we think each part is
        weight_distance = 6
        weight_car_velocity = 3
        weight_ball_velocity = 5
        weight_facing = 1

        #print(f"ball: {normalized_distance_me}, car: {normalized_velocity_me}, ball: {normalized_velocity_ball_me}, facing: {facing_factor_me}")
        #print(f"ball: {normalized_distance_friend}, car: {normalized_velocity_friend}, ball: {normalized_velocity_ball_friend}, facing: {facing_factor_friend}")
        me_score = (weight_distance * normalized_distance_me) + (weight_car_velocity * normalized_velocity_me) + (weight_ball_velocity * normalized_velocity_ball_me) + (weight_facing * facing_factor_me)
        friend_score = (weight_distance * normalized_distance_friend) + (weight_car_velocity * normalized_velocity_friend) + (weight_ball_velocity * normalized_velocity_ball_friend) + (weight_facing * facing_factor_friend)
        #print(f"my score: {me_score}, their score: {friend_score}")
        if me_score >= friend_score:
            return False
        else:
            return True
    else:
        return False

