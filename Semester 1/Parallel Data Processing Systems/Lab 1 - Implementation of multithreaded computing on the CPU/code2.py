import multiprocessing.process
from PIL import Image
import numpy as np
import threading
import multiprocessing
import time
import cv2

kernel_relief = np.array([[-2, -1, 0],
                          [-1,  1, 1],
                          [ 0,  1, 2]])

#images = ['collage 10240.png']
images = ['collage 10240.png','cruella 20480.jpg','iceland 12800.jpg']

threads_quantities = [1, 2, 4, 6, 8, 12]

# Разделение матрицы на две части
def split_matrix(matrix, parts_quantity):
    indexes = []
    parts = []
    for i in range(parts_quantity+1):
        indexes.append((matrix.shape[0]//parts_quantity)*i)

    i = 0
    while (i < parts_quantity):
        parts.append(matrix[indexes[i]:indexes[i+1]])
        i += 1
    
    return parts

def not_mine_convolution(index, image_part, kernel, result):
    convoluted_image = cv2.filter2D(image_part, -1, kernel)
    result[index] = convoluted_image


for threads_quantity in threads_quantities:
    if __name__ == '__main__':
        time_diffs = []
        times_stages = []
        time_stage = 0
        for i in range(5):
            for image_name in images:
                image = cv2.imread(image_name, cv2.IMREAD_COLOR)
                print(f'image: {image_name}, image shape: {image.shape}')
                parts = split_matrix(image, threads_quantity)
                print(f'parts count: {len(parts)}, shape of one part: {parts[0].shape}')
                
                with multiprocessing.Manager() as manager:
                    processes = []
                    # Инициализация списка для результатов с фиксированным размером
                    result_list = manager.list([None] * threads_quantity)
                    
                    start_time = time.time()
                    for index, part in enumerate(parts):
                        process = multiprocessing.Process(target=not_mine_convolution, args=(index, part, kernel_relief, result_list))
                        processes.append(process)
                    
                    for process in processes:
                        process.start()

                    for process in processes:
                        process.join()
                    end_time = time.time()
                    final_image = np.vstack(list(result_list))

                time_diffs.append(end_time - start_time)
                if (len(time_diffs) == 3):
                    for tim_diff in time_diffs:
                        time_stage += tim_diff
                    times_stages.append(time_stage)
                    time_diffs.clear()
                    time_stage = 0
                #print(f'added_to_times: {end_time - start_time}')
                final_image_name = image_name + '_convoluted.jpg'
                cv2.imwrite(final_image_name, final_image)
            
            #print(f'processes: {threads_quantity}\n')
        print(f'processes: {threads_quantity}')
        for time_diff in times_stages:
            print(f'task_time = {time_diff}')