import random, numpy as np
import pandas as pd
# 1 вверх 2 вниз 3 влево 4 вправо 5 стоять

ALPHA = 0.1 # Learning rate of Q learning
GAMMA = 0.9 # Discount factor of Q learning

class Agent:
    def __init__(self, env_map, start_pos, goal_position, replaced_value):
        self.map = env_map
        self.pos = start_pos
        self.goal = goal_position
        self.last_replaced_value = replaced_value
        self.q_df = pd.DataFrame(columns=['TOP', 'BOTTOM', 'LEFT', 'RIGHT', 'STOP'])
        self.q_df.index = pd.MultiIndex.from_tuples([], names=["row", "column"])  # Пустой MultiIndex

    def choose_action(self, available_movements: list) -> str:  
        action = random.randrange(len(available_movements))
        action = available_movements[action]
        return action
    
    def calculate_Q_val(self, old_pos, new_pos, action, reward):
        old_pos = (old_pos[0][0], old_pos[1][0])
        new_pos = (new_pos[0][0], new_pos[1][0])
        

        max_value = self.q_df.loc[new_pos].max()
        q_value = ALPHA * (reward + GAMMA*max_value - q)
        if action == 'TOP':
            q_value = 
            self.q_table[1] = val

        self

        pass
    
    def get_pos(self) -> tuple:
        return self.pos
    
    def get_metric(self):
        return ((self.goal[0][0] - self.pos[0][0]) ** 2 + (self.goal[1][0] - self.pos[1][0]) ** 2) ** (1/2)
        

    def update_position(self, pos: tuple, reward):
        self.pos = pos

        
    


        
