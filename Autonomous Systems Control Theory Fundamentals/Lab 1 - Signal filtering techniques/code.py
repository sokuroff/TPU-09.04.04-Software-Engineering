import numpy as np
import matplotlib.pyplot as plt

ALPHA = 0.1
N = 4

def Exponential_smoothing_filter(a):
    y = a.copy()
    for i in range(1, y.size):
        y[i] = ALPHA * y[i] + (1-ALPHA) * y[i-1]
    return y

def Simple_moving_average_filter(a):
    y = a.copy()
    




x = np.linspace(-4*np.pi, 4*np.pi, 800)
y = np.sin(x)
noise = np.random.normal(0,0.05,800)
y += noise
spikes = np.random.choice([0, 1], size=x.shape, p=[0.98, 0.02])  # Случайные всплески (2% вероятность)
amplitude = np.random.uniform(-1, 1, size=x.shape)  # Случайная амплитуда всплесков
y += noise + spikes * amplitude
y_exp = Exponential_smoothing_filter(y)
plt.figure(figsize=[8,3])
plt.plot(x,y)
plt.plot(x,y_exp)
plt.grid()
ax = plt.gca()
ax.set_xlim([-4*np.pi,4*np.pi])
ax.set_ylim([-2,2])
 



plt.show()
