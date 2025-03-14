import matplotlib as plt, random, os
import numpy as np
import random
from environment import Environment
from agent import Agent
# Global variables

ITERATIONS = 1000

# method to save the Q table in order to load it later in another run
def save_table():
    import pandas as pd
    # Загрузка CSV-файла с учетом разделителя ';'
    df = pd.read_csv('table.csv', sep=';')

    # Приводим 'row' и 'column' к числовому типу
    df['row'] = df['row'].astype(int)
    df['column'] = df['column'].astype(int)

    # Создаем сводную таблицу
    pivot_table = df.set_index(['row', 'column'])[['TOP', 'BOTTOM', 'LEFT', 'RIGHT']]

    # Открываем CSV-файл для записи
    with open('formatted_table.csv', 'w', encoding='utf-8') as f:
        # Записываем заголовки столбцов
        columns = sorted(df['column'].unique())
        f.write('row;' + ';'.join(map(str, columns)) + '\n')

        # Записываем данные построчно
        for row in sorted(df['row'].unique()):
            row_values = []
            for col in columns:
                values = pivot_table.xs((row, col), level=['row', 'column']).values
                cell_text = ','.join(map(str, values))  # Через запятую
                # cell_text = '\n'.join(map(str, values))  # Вертикальный вариант
                row_values.append(f'"{cell_text}"')  # Оборачиваем в кавычки для корректной обработки CSV
            f.write(f'{row};' + ';'.join(row_values) + '\n')


#----------------------------------Main function-------------------------------

if __name__ == '__main__':
    # initialization
    env_map = Environment('map.txt') # load the map
    start_pos, replaced_value, goal = env_map.get_info_for_creating_agent() # get start pos and goal of the main agent
    agent = Agent(map, start_pos, goal, replaced_value) # create an agent with this info
    env_map.create_agent(agent)  # and add agent to the map
    

    

    # course of time
    for iter in range(ITERATIONS):
        agent_action = agent.choose_action(env_map.get_possible_movements(agent.pos)) # get action from the possible on  es
        env_map.move_agent(agent, agent_action) # after we get an action we transmit it to environment in order to move the agent
        agent.update_position(env_map.get_agent_pos(), agent_action) # and then we tell to agent that his position changed
        print(f'Iteration:  {iter}')
        print(f'Distance to goal:  {agent.get_metric()}')
        print('-------------------------------------')

        # success we got him to the point
        if (agent.pos == env_map.goal):
            break
    agent.q_df.to_csv("table.csv", sep = ';', decimal = ',')  # Экспорт в CSV
save_table()
