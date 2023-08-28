from routines import *

#Detects Kickoff spawn, compares it to friends and then chooses a strategy
def detect_kickoff_spawn(agent):
    #avoids potential problems
    closest_kickoff = False
    #Checks if we are left
    if (agent.me.location[0] > 0 and agent.me.location[1] < 0) or (agent.me.location[0] < 0 and agent.me.location[1] > 0):
        is_left = True
    else:
        is_left = False
    #Finds if we are the closest or closest with someone else and left
    my_distance_to_ball = (agent.me.location - agent.ball.location).magnitude()
    closest_distance_to_ball = float('inf')
    for friend in agent.friends:
        friend_distance_to_ball = (friend.location - agent.ball.location).magnitude()
        closest_distance_to_ball = min(closest_distance_to_ball, friend_distance_to_ball)
    if my_distance_to_ball < closest_distance_to_ball or (my_distance_to_ball == closest_distance_to_ball and is_left):
        closest_kickoff = True
    return closest_kickoff

#Detecs any boost in front of the agent
def detect_boost(agent):
    angle_threshold = math.radians(45)
    forward_vector = agent.me.forward
    cos_angle_threshold = math.cos(angle_threshold)
    boosts_in_front = [boost for boost in agent.boosts if boost.active and forward_vector.dot(boost.location - agent.me.location) >= cos_angle_threshold]
    closest_boost = None
    closest_boost_distance = float('inf')

    # Iterate through the boosts in front and find the closest one
    for boost in boosts_in_front:
        boost_distance = (boost.location - agent.me.location).magnitude()
        if boost_distance < closest_boost_distance:
            closest_boost = boost
            closest_boost_distance = boost_distance
    take_closest_boost_within_60deg = closest_boost_distance < 1000

    return take_closest_boost_within_60deg, closest_boost

#Finds the nearest biggest boost
def big_boost(agent):
    big_boost = [boost for boost in agent.boosts if boost.large and boost.active]
    closest_big_boost = None
    closest_big_boost_distance = float('inf')

    for boost in big_boost:
        boost_distance = (boost.location - agent.me.location).magnitude()
        if boost_distance < closest_big_boost_distance:
            closest_big_boost = boost
            closest_big_boost_distance = boost_distance

    return closest_big_boost

def target_positions_off_ball(agent):

    ball_y_position = agent.ball.location[1]
    orange_goal_y_position = 5120
    blue_goal_y_position = -5120
    distance_blue_ball = (blue_goal_y_position - agent.ball.location[1])
    distance_orange_ball = (orange_goal_y_position - agent.ball.location[1])

    #Can easily add / change the target locations by adding / changing these values
    percentages = {
        "ahead": -0.2,
        "pushed_up": 0.2,
        "half_way": 0.5,
        "defensive": 0.8
    }
    #this uses the blue pov. So for orange its reversed
    x_values = {
        "far_left": 3800,
        "left": 1900,
        "center": 0,
        "right": -1900,
        "far_right": -3800,
    }
    #execute code if team == 0 (blue)
    if agent.team == 0:
        y_targets_blue = []
        for key, percentage in percentages.items():
            target_y = distance_blue_ball * percentage
            y_targets_blue.append({key: target_y})

        #creating targets blue team
        y_values = []
        for target_dict in y_targets_blue:
            for key, target in target_dict.items():
                target_locations = ball_y_position + target
                y_values.append({key: target_locations})

    #!!!This should include code "if y > 5100 then y 5100"!!!
        print(y_values)
        target_positions = []
        # Iterate through x and y values to create target locations
        for x_key, x_value in x_values.items():
            for y_dict in y_values:
                for y_key, y_value in y_dict.items():
                    target_position = Vector3(x_value, y_value, 0)
                    target_positions.append({
                        "x_key": x_key,
                        "y_key": y_key,
                        "position": target_position
                    })

    #execude code if team != 0 (orange)
    if agent.team != 0:
        y_targets_orange = []
        for key, percentage in percentages.items():
            target_y = distance_orange_ball * percentage
            y_targets_orange.append({key: target_y})

        # creating targets blue team
        y_values = []
        for target_dict in y_targets_orange:
            for key, target in target_dict.items():
                target_locations = ball_y_position + target
                y_values.append({key: target_locations})

    #!!!This should include code "if y > 5100 then y 5100"!!!
        target_positions = []
        # Iterate through x and y values to create target locations
        for x_key, x_value in x_values.items():
            for y_dict in y_values:
                for y_key, y_value in y_dict.items():
                    target_position = Vector3(x_value, y_value, 0)
                    target_positions.append({
                        "x_key": x_key,
                        "y_key": y_key,
                        "position": target_position
                    })

    #This Prints all the target locations for use later.
    #It starts of with 1y and then goes through all x values.
    #1y1x[0] 1y2x[1] 1y3x[2]...
    #2y1x[4] 2y2x[5]...
    #3y1x[8]...
    #!!!Note that from blue's pov the x_values go from left to right while from orange's pov it goes from right to left!!!
    #print(target_positions)
    return target_positions
