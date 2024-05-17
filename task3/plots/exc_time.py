import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt


# Отрисовка времени выполнения
def plot_exc_times(exc_t: ndarray, N: ndarray, names: ndarray, colors: ndarray) -> None:
    # Отрисовка погрешностей
    plt.figure(figsize=(7, 7))     
    plt.rc('axes', titlesize= 10)
    legend_str = []
    
    # Рисую по методам
    for i in range(names.shape[0]):
        plt.plot(N, exc_t[:, i], color = colors[i], label=names[i])
        legend_str.append(names[i])
    
    plt.title('Время выполнения программы')
    plt.xlabel('$N тел$')
    plt.ylabel('$t$')
    plt.legend(legend_str)