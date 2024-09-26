from PIL import Image
import numpy as np
import threading
import time

kernel_relief = np.array([[-2, -1, 0],
                          [-1,  1, 1],
                          [ 0,  1, 2]])


padding = 0
stride = 1

threads_quantity = 16

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

def get_rgb_matrices(image_path):
    image = Image.open(image_path)
    image_np = np.array(image)
    red_channel = green_channel = blue_channel = 0
    if (image_np.ndim == 3):
        red_channel = image_np[:,:,0]
        green_channel = image_np[:,:,1]
        blue_channel = image_np[:,:,2]
    return (red_channel, green_channel, blue_channel)


def constant_zero_padding(input_arr):
    """
    function to generate 0 padding around input array

    Parameter
    ---------
    input_arr : arr
        The array to which padding wil be added
    
    Returns
    -------
    output : arr
        The input_arr with paddings
    """
    output = np.zeros((input_arr.shape[0]+2, input_arr.shape[1]+2), dtype=int)

    for i in range(input_arr.shape[0]):
        for j in range(input_arr.shape[1]):
            output[i+1][j+1] = input_arr[i,j]
    return output

def convolution(kernel, input_arr, padding, stride):
    """
    function which produces convuliton operation on input_arr
    
    Parameters
    ----------
    kernel : arr
        The kernel which used in convolution, must be smaller than input_arr
    input_arr : arr
        The array which will be convoluted, must be bigger than kernel
    padding : int
        '1' is to create const zero padding around array in order to make 
        output array the same scale as the input one and '0' to not do it.
    stride : int
        step by which the convolution opeartion is shifted through 
        input_arr. But for now it's uses only to define output array sizes

    Returns
    -------
    output_arr
        convoluted array
    """
    frame = np.zeros_like(kernel)
    kernel_size = kernel.shape[0]
    rows_num = input_arr.shape[0]
    column_num = input_arr.shape[1]
    output_height=((rows_num-kernel_size+2*padding)/stride)+1
    output_width=((column_num-kernel_size+2*padding)/stride)+1
    output_arr = np.zeros((int(output_height),int(output_width)), dtype=int)

    i = j = k = l = val = 0

    while k < output_arr.shape[0]:
        while l < output_arr.shape[1]:
            while i < kernel_size:
                while j < kernel_size:
                    frame[i][j] = input_arr[i+k][j+l] 
                    j += 1

                j = 0
                i += 1

            if (i == kernel_size): 
                for m in range(frame.shape[0]):
                    for n in range(frame.shape[1]):
                        val += frame[m][n]*kernel_relief[m][n]  
            output_arr[k][l] = val
            val = j = i = 0
            l += 1         
        l = 0
        k += 1
    return output_arr


r, g, b = get_rgb_matrices('C:/Users/Ruslan/Desktop/TPU-09.04.04-Software-Engineering/Semester 1/Parallel Data Processing Systems/Lab 1 - Implementation of multithreaded computing on the CPU/collage 10240.png')
list = []
threads = []
start_time = time.time()

list = split_matrix(r, threads_quantity)
for i in list:
    threads.append(threading.Thread(target=convolution, args=(kernel_relief, i, padding, stride)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
end_time = time.time()    
print(f'time: {end_time - start_time}\n')
print(f'threads: {threads_quantity}\n')

# print(r.shape)
# print(r1.shape)
# print(r2.shape)
# t1 = threading.Thread(target=convolution, args=(kernel_relief, r1, padding, stride))
# t2 = threading.Thread(target=convolution, args=(kernel_relief, r2, padding, stride))

# # Запуск потоков
# t1.start()
# t2.start()
# # Ожидание завершения обоих потоков
# t1.join()
# t2.join()

# print('done')

# image = [r,g,b]
