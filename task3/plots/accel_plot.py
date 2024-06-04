import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt


# Отрисовка ускорений двух методов относительно тертьего
def plot_accel_times(exc_t: ndarray, N: ndarray, names: ndarray, colors: ndarray) -> None:
    # Отрисовка погрешностей
    plt.figure(figsize=(7, 7))     
    plt.rc('axes', titlesize= 10)
    legend_str = []
    
    # Рисую по методам
    plt.plot(N, exc_t[:, 0] / exc_t[:, 1], color = colors[0], label=names[0])
    legend_str.append(names[0])

    plt.plot(N, exc_t[:, 2] / exc_t[:, 1], color = colors[1], label=names[1])
    legend_str.append(names[1])
    
    plt.title('Ускорение относительно multiprocessing')
    plt.xlabel('$N тел$')
    plt.ylabel('$a$')
    plt.legend(legend_str)