import matplotlib as plt, random, os
import numpy as np
import random
# Global variables

ITERATIONS = 10
AGENT_ACTIONS = ['LEFT', 'RIGHT', 'TOP', 'BOTTOM', 'STOP']



def show_map(map):
    map_str = '\n'.join([''.join(row) for row in map])
    print(map_str)

def create_main_agent(map):
    start_pos = np.where(map == '2')
    map[start_pos] = 'A'
    return map

def get_possible_movements(map, idx):
    available_positions = []

    # Check if the top neighbour exists (idx[0] > 0 to avoid out of bounds)
    if idx[0] > 0:
        top_neighbour = map[idx[0] - 1][idx[1]]
        available_positions.append((idx[0] - 1, idx[1]))  # Add to available positions
    
    # Check if the bottom neighbour exists (idx[0] < len(map) - 1 to avoid out of bounds)
    if idx[0] < len(map) - 1:
        bottom_neighbour = map[idx[0] + 1][idx[1]]
        available_positions.append((idx[0] + 1, idx[1]))  # Add to available positions
    
    # Check if the left neighbour exists (idx[1] > 0 to avoid out of bounds)
    if idx[1] > 0:
        left_neighbour = map[idx[0]][idx[1] - 1]
        available_positions.append((idx[0], idx[1] - 1))  # Add to available positions
    
    # Check if the right neighbour exists (idx[1] < len(map[0]) - 1 to avoid out of bounds)
    if idx[1] < len(map[0]) - 1:
        right_neighbour = map[idx[0]][idx[1] + 1]
        available_positions.append((idx[0], idx[1] + 1))  # Add to available positions
    
    return available_positions




with open('map.txt', 'r') as file:
    map_str = file.read()


# Convert string to a 2D list of characters
map = [list(line) for line in map_str.split('\n')]
# Convert to a NumPy array for easier manipulation
map = np.array(map)

map = create_main_agent(map)

show_map(map)

agent_pos = np.where(map == 'A')
available_actions = get_possible_movements(map, agent_pos)
print(available_actions)

# for iter in range(ITERATIONS):
#     action = AGENT_ACTIONS[random.randrange(5)]
    
#     if action == 'TOP':

#     pass
# print(map)