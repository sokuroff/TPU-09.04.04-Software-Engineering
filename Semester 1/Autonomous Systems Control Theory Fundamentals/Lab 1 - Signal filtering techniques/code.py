# Подключение необходимых библиотек
import numpy as np
import matplotlib.pyplot as plt

# Установление зерна случайно генерации
# Для возобнавляемости экспериментов
np.random.seed(52)  

# Постоянные переменыые
ALPHAS = [0.1, 0.25, 0.5] # Степень влияния прошлых значений для Exponential_smoothing_filter
N = [8, 16, 32] # Используется в скользящем среднем и медианном фильтрах
THRESHOLDS = [0.05, 0.1, 0.2] # Порог скорости нарастания сигнала

# Настройки шрифта для графика
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14

# -------------------------------------  Создание функции каждого фильтра  -----------------------------------#
def Exponential_smoothing_filter(data, alpha):
    """
    Функция реализации фильтра экспоненциального сглаживания
    
    :param a: массив данных, которые нужно отфильтровать
    :param alpha: регулировочный коэффициент
    :return: отфильтрованный массив
    """
    filtered_data = data.copy()
    for i in range(1, filtered_data.size):
        filtered_data[i] = alpha * filtered_data[i] + (1-alpha) * filtered_data[i-1]
    return filtered_data

def moving_average_filter(data, n):
    """
    Функция реализации фильтра скользящего среднего
    
    :param data: массив данных, которые нужно отфильтровать
    :param n: ширина окна усреднения
    :return: отфильтрованный массив
    """
    # Массив для хранения отфильтрованных значений
    filtered_data = []

    # Массив для хранения текущего окна измерений
    current_values = []

    # Пройдем по всем элементам исходного массива
    for new_value in data:
        # Добавляем текущее новое значение в массив измерений
        current_values.append(new_value)
        
        # Если количество элементов меньше n, считаем среднее по всем доступным значениям
        if len(current_values) < n:
            avg = np.mean(current_values)
        else:
            # Как только элементов стало n или больше, считаем среднее по последним n значениям
            avg = np.mean(current_values[-n:])
        
        # Добавляем отфильтрованное значение в результат
        filtered_data.append(avg)

    return filtered_data

def median_filter(data, window_size):
    """
    Функция реализации медианного фильтра
    
    :param data: массив данных, которые нужно отфильтровать
    :param n: ширина окна расчёта медианы
    :return: отфильтрованный массив
    """
    # Если размер окна меньше 1 или больше длины сигнала, возвращаем исходный сигнал
    if window_size < 1 or window_size > len(data):
        return data
    
    # Создаем список для хранения отфильтрованных значений
    filtered_data = []
    
    half_window = window_size // 2
    
    # Проходим по каждому элементу сигнала
    for i in range(len(data)):
        # Выбираем окно вокруг текущего элемента
        start_idx = max(0, i - half_window)
        end_idx = min(len(data), i + half_window + 1)
        
        # Получаем подмассив, сортируем его и находим медиану
        window = sorted(data[start_idx:end_idx])
        
        # Если окно нечетное, выбираем центральный элемент
        if window_size % 2 == 1:
            median = window[len(window) // 2]
        else:
            # Если окно четное, берем среднее арифметическое двух центральных элементов
            mid1 = window[len(window) // 2 - 1]
            mid2 = window[len(window) // 2]
            median = (mid1 + mid2) / 2.0
        
        # Добавляем медиану в отфильтрованный сигнал
        filtered_data.append(median)
    
    return np.array(filtered_data)

def rate_limit_filter(data, threshold):
    """
    Функция реализации функции ограниченной скорости нарастания сигнала
    
    :param data: массив данных, которые нужно отфильтровать
    :param threshold: пороговое значение скорости нарастания
    :return: отфильтрованный массив
    """
    
    # Инициализация массива выходного сигнала
    filtered_data = [data[0]]
    
    # Применение фильтра
    for i in range(1, len(data)):
        delta = data[i] - data[i-1]
        if abs(delta) <= threshold:
            filtered_data.append(data[i])
        else:
            # Ограничение прироста
            if delta > 0:
                filtered_data.append(filtered_data[-1] + threshold)
            else:
                filtered_data.append(filtered_data[-1] - threshold)
    
    return filtered_data


# ---------------------  Создание чистого и зашумленного сигналов для дальнейших эксериментов -------------------#
x = np.linspace(-4*np.pi, 4*np.pi, 800) # Создание массива иксов
y = np.sin(x) # Функция
y_clean = np.sin(x)
noise = np.random.uniform(-0.1,0.1,800) # Добавляем равномерно распределенный шум
spikes = np.random.choice([0, 1], size=x.shape, p=[0.98, 0.02])  # Случайные всплески (2% вероятность)
amplitude = np.random.uniform(-1, 1, size=x.shape)  # Случайная амплитуда всплесков
y += noise + spikes * amplitude # дальше наш сигнал это зашумлённый сигнал



# ---------------------  Вывод на график результата фильтрации (нужный раскоментить)  ----------------------------#

#y_exp = Exponential_smoothing_filter(y)
# plt.figure(figsize=[8,3])
# plt.plot(x,y, color='gray', linewidth=3, label='Зашумлённый сигнал')
# plt.plot(x,y_clean, color='black', linewidth=1.5, label='Оригинальный сигнал')
# plt.grid()
# ax = plt.gca()
# ax.set_xlim([-4*np.pi,4*np.pi])
# ax.set_ylim([-1.5,3])
# plt.xlabel('x')
# plt.ylabel('y') 
# plt.legend()

# ---------------------  Вывод на график результата фильтрации (нужный раскоментить)  ----------------------------#

# plt.figure(figsize=[8, 9])  # Размер всей фигуры: 8x9 (3 графика по 8x3)

# for idx, alpha in enumerate(ALPHAS):
#     y_exp = Exponential_smoothing_filter(y, alpha)
#     plt.subplot(len(ALPHAS), 1, idx + 1)
#     plt.plot(x, y, color='gray', linewidth=3, label='Зашумлённый сигнал')
#     plt.plot(x, y_exp, color='black', linewidth=1.5, label=f'Отфильтрованный сигнал')
#     plt.grid()
#     plt.xlim([-4 * np.pi, 4 * np.pi])
#     plt.ylim([-1.5, 4])
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.legend()
#     plt.title(f'Отфильтрованный сигнал, α = {alpha}')

# plt.tight_layout()

# ---------------------  Вывод на график результата фильтрации (нужный раскоментить)  ----------------------------#

# plt.figure(figsize=[8, 9])  # Размер всей фигуры: 8x9 (3 графика по 8x3)

# for idx, n in enumerate(N):
#     y_exp = moving_average_filter(y, n)
#     plt.subplot(len(N), 1, idx + 1)
#     plt.plot(x, y, color='gray', linewidth=3, label='Зашумлённый сигнал')
#     plt.plot(x, y_exp, color='black', linewidth=1.5, label=f'Отфильтрованный сигнал')
#     plt.grid()
#     plt.xlim([-4 * np.pi, 4 * np.pi])
#     plt.ylim([-1.5, 4])
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.legend()
#     plt.title(f'Отфильтрованный сигнал, n = {n}')

# plt.tight_layout()

# ---------------------  Вывод на график результата фильтрации (нужный раскоментить)  ----------------------------#

# plt.figure(figsize=[8, 9])  # Размер всей фигуры: 8x9 (3 графика по 8x3)

# for idx, n in enumerate(N):
#     y_exp = median_filter(y, n)
#     plt.subplot(len(N), 1, idx + 1)
#     plt.plot(x, y, color='gray', linewidth=3, label='Зашумлённый сигнал')
#     plt.plot(x, y_exp, color='black', linewidth=1.5, label=f'Отфильтрованный сигнал')
#     plt.grid()
#     plt.xlim([-4 * np.pi, 4 * np.pi])
#     plt.ylim([-1.5, 4])
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.legend()
#     plt.title(f'Отфильтрованный сигнал, n = {n}')

# plt.tight_layout()

# ---------------------  Вывод на график результата фильтрации (нужный раскоментить)  ----------------------------#

# plt.figure(figsize=[8, 9])  # Размер всей фигуры: 8x9 (3 графика по 8x3)

# for idx, threshold in enumerate(THRESHOLDS):
#     y_exp = rate_limit_filter(y, threshold)
#     plt.subplot(len(THRESHOLDS), 1, idx + 1)
#     plt.plot(x, y, color='gray', linewidth=3, label='Зашумлённый сигнал')
#     plt.plot(x, y_exp, color='black', linewidth=1.5, label=f'Отфильтрованный сигнал')
#     plt.grid()
#     plt.xlim([-4 * np.pi, 4 * np.pi])
#     plt.ylim([-1.5, 4])
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.legend()
#     plt.title(f'Отфильтрованный сигнал, threshold = {threshold}')

# plt.tight_layout()

# ---------------------  Вывод на график результата фильтрации (нужный раскоментить)  ----------------------------#

y_med = median_filter(y, 32)
y_exp = Exponential_smoothing_filter(y_med, 0.25)
plt.figure(figsize=[8,3])
plt.plot(x,y, color='gray', linewidth=3, label='Зашумлённый сигнал')
plt.plot(x,y_exp, color='black', linewidth=1.5, label='Отфильтрованный сигнал')
plt.grid()
ax = plt.gca()
ax.set_xlim([-4*np.pi,4*np.pi])
ax.set_ylim([-1.5,3])
plt.xlabel('x')
plt.ylabel('y') 
plt.legend()

plt.show()
