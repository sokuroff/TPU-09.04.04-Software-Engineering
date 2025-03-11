import matplotlib as plt, random, os
import numpy as np
import random
# Global variables

ITERATIONS = 10
AGENT_ACTIONS = ['LEFT', 'RIGHT', 'TOP', 'BOTTOM', 'STOP']

def move_agent(map, action, last_replaced_value):
    if action == 'LEFT':
        agent_pos = get_agent_pos(map)
        map[agent_pos] = last_replaced_value
        last_replaced_value = map[agent_pos[0], agent_pos[1] - 1]
        map[agent_pos[0], agent_pos[1] - 1] = 'A'
    elif action == 'RIGHT':
        agent_pos = get_agent_pos(map)
        map[agent_pos] = last_replaced_value
        last_replaced_value = map[agent_pos[0], agent_pos[1] + 1]
        map[agent_pos[0], agent_pos[1] + 1] = 'A'
    elif action == 'TOP':
        agent_pos = get_agent_pos(map)
        map[agent_pos] = last_replaced_value
        last_replaced_value = map[agent_pos[0] - 1, agent_pos[1]]
        map[agent_pos[0] - 1, agent_pos[1]] = 'A'
    elif action == 'BOTTOM':
        agent_pos = get_agent_pos(map)
        map[agent_pos] = last_replaced_value
        last_replaced_value = map[agent_pos[0] + 1, agent_pos[1]]
        map[agent_pos[0] + 1, agent_pos[1]] = 'A'
    
    return map, main_agent_replaced_value





#----------------------------------Main function-------------------------------

if __name__ == '__main__':
    map, goal_position = create_map()
    map, main_agent_replaced_value = create_main_agent(map, main_agent_replaced_value)

    for iter in range(ITERATIONS):
        available_movements = get_possible_movements(map, get_agent_pos(map))
        action = random.randrange(0, len(available_movements))
        map, main_agent_replaced_value = move_agent(map, available_movements[action], main_agent_replaced_value)
        print(f'Iteration:  {iter}')
        print(f'Distance to goal:  {get_metric(get_agent_pos(map), goal_position)}')
        print('-----------------------------------')
    

