import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import fenics
import string
from func_lib.get_errors import get_errors
from typing import List

def plot_sol(mesh: fenics.Mesh, solution, title_str: string) -> None:
    n = mesh.num_vertices()
    d = mesh.geometry().dim()

    mesh_coordinates = mesh.coordinates().reshape((n, d))
    triangles = np.asarray([cell.entities(0) for cell in fenics.cells(mesh)])
    triangulation = tri.Triangulation(mesh_coordinates[:, 0], mesh_coordinates[:, 1], triangles)

    plt.figure(figsize = (6, 5))
    zfaces = np.asarray([solution(cell.midpoint()) for cell in fenics.cells(mesh)])
    plt.tripcolor(triangulation, facecolors = zfaces, edgecolors = 'k', cmap = 'jet')

    plt.title(title_str)
    plt.colorbar()
    plt.plot()
    plt.show()



def plot_errors(time_grid: np.ndarray, u_exact: fenics.Expression,
                num_sol_list: List[fenics.Function], mesh: fenics.Mesh) -> None:
    L2_err = []
    max_err = []

    for i in range(time_grid.shape[0]):
        u_exact.t = time_grid[i]
        error_L2, error_max = get_errors(u_exact, num_sol_list[i], mesh)
        L2_err.append(error_L2)
        max_err.append(error_max)
    
    # Строим график
    plt.figure(figsize=(8, 6))
    plt.plot(time_grid, L2_err, label='L2_error', color='blue')
    plt.plot(time_grid, max_err, label='max_error', color='green')
    
    # Добавляем заголовок, метки осей и легенду
    plt.title('Графики зависимости ошибок от времени')
    plt.xlabel('t')
    plt.ylabel('error')
    plt.legend()


    
    # Отображаем график
    plt.show()



