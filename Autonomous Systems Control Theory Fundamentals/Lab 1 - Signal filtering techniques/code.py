# Подключение необходимых библиотек
import numpy as np
import matplotlib.pyplot as plt

# Постоянные переменыые
ALPHA = 0.1 # Степень влияния прошлых значений для Exponential_smoothing_filter
N = 4

# Убедитесь, что у вас установлен шрифт Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14

def Exponential_smoothing_filter(a):
    y = a.copy()
    for i in range(1, y.size):
        y[i] = ALPHA * y[i] + (1-ALPHA) * y[i-1]
    return y

def Simple_moving_average_filter(a):
    y = a.copy()

    
x = np.linspace(-4*np.pi, 4*np.pi, 800) # Создание массива иксов
y = np.sin(x) # Функция
y_clean = np.sin(x)
noise = np.random.uniform(-0.1,0.1,800) # Добавляем равномерно распределенный шум
spikes = np.random.choice([0, 1], size=x.shape, p=[0.98, 0.02])  # Случайные всплески (2% вероятность)
amplitude = np.random.uniform(-1, 1, size=x.shape)  # Случайная амплитуда всплесков
y += noise + spikes * amplitude # дальше наш сигнал это зашумлённый сигнал
y_exp = Exponential_smoothing_filter(y)
plt.figure(figsize=[8,3])
plt.plot(x,y, color='gray', linewidth=1.5, label='Зашумлённый сигнал')
plt.plot(x,y_clean, color='black', linewidth=0.8, label='Оригинальный сигнал')
plt.grid()
ax = plt.gca()
ax.set_xlim([-4*np.pi,4*np.pi])
ax.set_ylim([-1.5,3])
plt.xlabel('x')
plt.ylabel('y') 
plt.legend()


plt.show()
