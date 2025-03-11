import matplotlib as plt, random, os
import numpy as np
import random



from agent import Agent
# Global variables

ITERATIONS = 10
AGENT_ACTIONS = ['LEFT', 'RIGHT', 'TOP', 'BOTTOM', 'STOP']

class Environment():
    def __init__(self, filename):
        self.map, self.goal = self.load_map(filename)
    
    def load_map(filename):
        with open(filename, 'r') as file:
            map_str = file.read()

        # Convert string to a 2D list of characters
        map = [list(line) for line in map_str.split('\n')]
        # Convert to a NumPy array for easier manipulation
        map = np.array(map)
        goal_position = np.where(map == '4')
        return map, goal_position
    
    def show_map(self):
        map_str = '\n'.join([''.join(row) for row in self.map])
        print(map_str)

    def get_agent_pos(self):
        agent_pos = np.where(self.map == 'A')
        return agent_pos

    def create_main_agent(self):
        start_pos = np.where(self.map == '2')
        replaced_value = self.map[start_pos]
        main_agent = Agent(self.map, start_pos, self.goal, replaced_value)
        self.map[start_pos] = 'A'
        return main_agent
    
    def get_possible_movements(self, pos: tuple) -> list:
        available_moves = []
        row = pos[0][0]
        column = pos[1][0]

        top_neighbour = self.map[row - 1][column] if row > 0 else None
        if top_neighbour is not None and top_neighbour != '1':
            available_moves.append('TOP')
        
        bottom_neighbour = self.map[row + 1][column] if row < len(self.map) - 1 else None
        if bottom_neighbour is not None and bottom_neighbour != '1':
            available_moves.append('BOTTOM')

        left_neighbour = self.map[row][column - 1] if column > 0 else None
        if left_neighbour is not None and left_neighbour != '1':
            available_moves.append('LEFT')
        
        right_neighbour = self.map[row][column + 1] if column < len(self.map[0]) - 1 else None
        if right_neighbour is not None and right_neighbour != '1':
            available_moves.append('RIGHT')
        
        return available_moves