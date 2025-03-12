import matplotlib as plt, random, os
import numpy as np
import random
from environment import Environment
from agent import Agent
# Global variables

ITERATIONS = 10

#----------------------------------Main function-------------------------------

if __name__ == '__main__':
    # initialization
    map = Environment('map.txt')
    start_pos, replaced_value, goal = map.get_info_for_creating_agent()
    agent = Agent(map, start_pos, goal, replaced_value)
    map.create_agent(agent)
    state = (map.get_agent_pos())
    state = (state[0][0], state[1][0])
    if state not in agent.q_df.index:
        agent.q_df.loc[state, :] = [0] * 5

    agent.q_df.loc[state, 'TOP'] = 2.2323
    print(agent.q_df)
    

    # course of time
    # for iter in range(ITERATIONS):
    #     reward = map.move_agent(agent, agent.choose_action(map.get_possible_movements(agent.pos)))
    #     agent.update_position(map.get_agent_pos(), reward)
    #     print(f'Iteration:  {iter}')
    #     print(f'Distance to goal:  {agent.get_metric()}')
    #     print('-------------------------------------')
    

