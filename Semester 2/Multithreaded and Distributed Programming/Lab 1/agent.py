import random, numpy as np
import pandas as pd
# 1 вверх 2 вниз 3 влево 4 вправо 5 стоять

EPSILON = 0.2 # for epsilon-greedy strategy
ALPHA = 0.05 # Learning rate of Q learning
GAMMA = 0.8 # Discount factor of Q learning

class Agent:
    def __init__(self, env_map, start_pos, goal_position, replaced_value):
        self.map = env_map
        self.pos = start_pos
        self.goal = goal_position
        self.last_replaced_value = replaced_value
        # Создание индексов
        rows = range(30)
        cols = range(30)
        multi_index = pd.MultiIndex.from_product([rows, cols], names=["row", "column"])
        # Создание DataFrame с нулями
        self.q_df = pd.DataFrame(0, index=multi_index, columns=['TOP', 'BOTTOM', 'LEFT', 'RIGHT', 'STOP'], dtype=np.float64)

    def choose_action(self, available_movements: list) -> str:
        rand_val = random.random()
        pos = (self.pos[0][0], self.pos[1][0])
        if rand_val < EPSILON: # exploration
            action = random.choice(available_movements)
        else: # exploitation
            available_q_values = self.q_df.loc[pos, available_movements]  # значения Q для доступных действий
            action = available_q_values.idxmax()  # действие с максимальным значением Q
        return action
    
    def calculate_Q_val(self, old_pos, new_pos, action, reward):
        old_pos = (old_pos[0][0], old_pos[1][0])
        new_pos = (new_pos[0][0], new_pos[1][0])
        
        max_value = self.q_df.loc[new_pos].max()
        if (self.q_df.loc[old_pos, action]) is not None:
            q = self.q_df.loc[old_pos, action]
        else:
            q = 0
        new_q_value = round(q + ALPHA * (reward + GAMMA*max_value - q), 2)
        print(f'new q value = {new_q_value}\n reward = {reward}')
        self.q_df.loc[old_pos, action] = new_q_value
    
    def get_pos(self) -> tuple:
        return self.pos
    
    def get_metric(self):
        return ((self.goal[0][0] - self.pos[0][0]) ** 2 + (self.goal[1][0] - self.pos[1][0]) ** 2) ** (1/2)

    def update_position(self, new_pos: tuple, action: str):
        old_pos = self.pos
        self.pos = new_pos
        reward = 100-self.get_metric()
        if self.q_df.loc[(new_pos[0][0], new_pos[1][0])].sum() != 0:  # Если сумма всех действий на данной позиции не равна нулю
            reward -= 150
        self.calculate_Q_val(old_pos, new_pos, action, reward)

        
    


        
