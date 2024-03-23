import matplotlib.pyplot as plt
import numpy as np

def one_plot_solution(ode_sol: np.ndarray, time_grid:np.ndarray) -> None:
    # Построение графика
    plt.title("Зависимости T[i](t)") # заголовок
    plt.xlabel("t")         # ось абсцисс
    plt.ylabel("T(t)")      # ось ординат
    plt.grid()              # включение отображения сетки

    legend_str = []
    for i in range(ode_sol.shape[1]):
        plt.plot(time_grid, ode_sol[:, i])  # построение графика
        legend_str.append("T[" + str(i + 1) + "](t)")
    plt.legend(legend_str)
    plt.show()
    return



def many_plot_solution(ode_sol: np.ndarray, time_grid:np.ndarray) -> None:
    num_elmnt = ode_sol.shape[1]
    # Построение графиков
    plt.figure(figsize=(9, 9))
    plt.rc('axes', titlesize= 10)

    # Построение графиков
    for i in range(num_elmnt):
        plt.subplot(3, 3, i + 1)
        plt.plot(time_grid, ode_sol[:, i])    # построение графика
        plt.xlabel("t")         # ось абсцисс
        plt.title("T[" + str(i + 1) + "](t)") # ось ординат
    plt.show()
    return

        