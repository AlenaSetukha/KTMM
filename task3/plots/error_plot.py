import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt

def get_error_to_ode(solve1: ndarray,
                     solve2: ndarray,
                     solve3: ndarray,
                     solve4: ndarray, 
                     time_grid: ndarray) -> None:
    
    N = solve3.shape[1]
    T = time_grid.shape[0]

    # Вычисление погрешности относительно odeint(solve1) и отрисовка
    # погрешность - евклидово расстояние между радиус-векторами
    error1 = []
    error2 = []
    error3 = []

    for i in range(T):
        tmp1 = []
        tmp2 = []
        tmp3 = []
        for j in range(N):
            tmp1.append(np.sqrt(np.sum(np.square([solve2[i, j * 6 + k] - solve1[i, j * 6 + k] for k in range(3)]))))
            tmp2.append(np.sqrt(np.sum(np.square([solve3[i, j, k] - solve1[i, j * 6 + k] for k in range(3)]))))
            tmp3.append(np.sqrt(np.sum(np.square([solve4[i, j, k] - solve1[i, j * 6 + k] for k in range(3)]))))
        error1.append(np.array(tmp1))
        error2.append(np.array(tmp2))
        error3.append(np.array(tmp3))

    error1 = np.array(error1)
    error2 = np.array(error2)
    error3 = np.array(error3)

    # Отрисовка погрешностей
    plt.figure(figsize=(7, 25))     
    plt.rc('axes', titlesize= 10)
    
    for i in range(N):
        plt.subplot(9, 1, i + 1)
        plt.plot(time_grid, error1[:, i], color = 'red', label='$|verle - ode|$')
        plt.plot(time_grid, error2[:, i], color = 'blue', label='$|mltp - ode|$')
        plt.plot(time_grid, error3[:, i], color = 'grey', label='$|cython - ode|$')
        plt.title('Погрешность для тела ' + str(i))
        plt.xlabel('$t$')
        plt.ylabel('$error$')
        plt.legend(['$|verle - ode|$', '$|mltp - ode|$', '$|cython - ode|$'])


