from tools import  *
from objects import *
from routines import *
from SubStrategy import *
from Information import *
from PlayerIntention import *
import random


#This file is for strategy

class LunaHusk(LunaHusk):
    def run(agent):

        if agent.name == "Luna Husk":
            agent.debug_stack()

        if len(agent.stack) <= 1:
            if agent.kickoff_flag:
                closest_kickoff = detect_kickoff_spawn(agent)
                print(closest_kickoff)
                if closest_kickoff is True:
                    print("Push KICKOFF")
                    agent.push(kickoff())
                else:
                    closest_big_boost = big_boost(agent)
                    agent.push(goto_boost(closest_big_boost,agent.ball.location))
            else:
                #The Default is to look if we can shoot. PlayerIntention.py will make sure we aren't double committing.
                targets = {"goal" : (agent.foe_goal.left_post, agent.foe_goal.right_post), "anywhere_but_our_net": (agent.friend_goal.right_post, agent.friend_goal.left_post)}
                shots = find_hits(agent,targets)
                if len(shots["goal"]) > 0 or len(shots["anywhere_but_our_net"]) > 0:
                    is_teammate_going_result = is_teammate_going(agent)
                    if len(shots["goal"]) > 0 and is_teammate_going_result == False:
                        print ("Shoot at Goal")
                        agent.push(shots["goal"][0])
                    elif len(shots["anywhere_but_our_net"]) > 0 and is_teammate_going_result == False:
                        print("Shoot Anywhere")
                        agent.push(shots["anywhere_but_our_net"][0])
                    else:
                        if not agent.me.boost > 20:
                            closest_big_boost = big_boost(agent)
                            agent.push(goto_boost(closest_big_boost,agent.friend_goal.location))
                        elif agent.me.boost > 20:
                            target_positions = target_positions_off_ball(agent)
                            random_entry = random.choice(target_positions)
                            x_key = random_entry['x_key']
                            y_key = random_entry['y_key']
                            random_position = random_entry['position']

                            print("PUSHING GOTONET")
                            agent.push(gotonet(random_position,agent.ball.location))
                        else:
                            print("!!!THIS SHOULDNT BE PRINTED!!!")
                else:
                    if not agent.me.boost > 20:
                        closest_big_boost = big_boost(agent)
                        agent.push(goto_boost(closest_big_boost,agent.friend_goal.location))
                    elif agent.me.boost > 20:
                        target_positions = target_positions_off_ball(agent)
                        random_entry = random.choice(target_positions)
                        x_key = random_entry['x_key']
                        y_key = random_entry['y_key']
                        random_position = random_entry['position']

                        print("PUSHING GOTONET")
                        agent.push(gotonet(random_position,agent.ball.location))
                    else:
                        print("!!!THIS SHOULDNT BE PRINTED!!!")

