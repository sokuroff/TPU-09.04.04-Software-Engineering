import random
import numpy as np



class Agent:
    def __init__(self, env_map, start_pos, goal_position, replaced_value):
        self.map = env_map
        self.pos = start_pos
        self.goal = goal_position
        self.last_replaced_value = replaced_value
        self.q_table = {}

    def choose_action(self, available_movements, agent_pos):
        pass
    
    def get_pos(self) -> tuple:
        return self.pos
    
    def get_metric(self):
        return ((self.goal[0][0] - self.pos[0][0]) ** 2 + (self.goal[1][0] - self.pos[1][0]) ** 2) ** (1/2)
    
    def make_move(self):
        available_movements = self.get_possible_movements(self.pos)
        self.choose_action()
        
