import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import fenics
import imageio
from typing import List


def create_gif_from_fenics_functions(time_grid: np.ndarray, mesh: fenics.Mesh,
                function_list: List[fenics.Function],
                output_file='output.gif'):
    max = 0
    min = 100

    # Чтобы гифка не "дергалась", зафиксируем верхнее и нижнее значение
    for i, function in enumerate(function_list):
        zfaces = np.asarray([function(cell.midpoint()) for cell in fenics.cells(mesh)])
            
        minimum = np.amin(zfaces)
        maximum = np.amax(zfaces)
        if (minimum < min):
            min = minimum
        if (maximum > max):
            max = maximum

    images = []

    # На каждом шаге создаем изображение, затем добавляем в гифку
    for i in range(time_grid.shape[0]):
        n = mesh.num_vertices()
        d = mesh.geometry().dim()

        mesh_coordinates = mesh.coordinates().reshape((n, d))
        triangles = np.asarray([cell.entities(0) for cell in fenics.cells(mesh)])
        triangulation = tri.Triangulation(mesh_coordinates[:, 0], mesh_coordinates[:, 1], triangles)

        plt.figure(figsize = (6, 5))
        zfaces = np.asarray([function_list[i](cell.midpoint()) for cell in fenics.cells(mesh)])
        plt.tripcolor(triangulation, facecolors = zfaces, edgecolors = 'k', cmap = 'jet')

        plt.clim(min, max)
        bounds = np.linspace(min, max, 10)

        plt.colorbar(ticks=bounds, boundaries = bounds)

        # Конвертация изображения в массив numpy.array
        fig = plt.gcf()
        fig.canvas.draw()
        image_array = np.array(fig.canvas.renderer.buffer_rgba())
        images.append(image_array)

        plt.close()


    # Сохраняем список изображений в виде гиф-изображения
    imageio.mimsave(output_file, images, duration=0.3)









def create_gif_from_fenics_expr(time_grid: np.ndarray, mesh: fenics.Mesh,
                sol_expr: fenics.Expression,
                output_file='output.gif'):
    max = 0
    min = 100

    # Чтобы гифка не "дергалась", зафиксируем верхнее и нижнее значение
    for i in range(time_grid.shape[0]):
        sol_expr.t = time_grid[i]
        zfaces = np.asarray([sol_expr(cell.midpoint()) for cell in fenics.cells(mesh)])
            
        minimum = np.amin(zfaces)
        maximum = np.amax(zfaces)
        if (minimum < min):
            min = minimum
        if (maximum > max):
            max = maximum

    images = []

    # На каждом шаге создаем изображение, затем добавляем в гифку
    for i in range(time_grid.shape[0]):
        n = mesh.num_vertices()
        d = mesh.geometry().dim()
        sol_expr.t = time_grid[i]

        mesh_coordinates = mesh.coordinates().reshape((n, d))
        triangles = np.asarray([cell.entities(0) for cell in fenics.cells(mesh)])
        triangulation = tri.Triangulation(mesh_coordinates[:, 0], mesh_coordinates[:, 1], triangles)

        plt.figure(figsize = (6, 5))
        zfaces = np.asarray([sol_expr(cell.midpoint()) for cell in fenics.cells(mesh)])
        plt.tripcolor(triangulation, facecolors = zfaces, edgecolors = 'k', cmap = 'jet')

        plt.clim(min, max)
        bounds = np.linspace(min, max, 10)

        plt.colorbar(ticks=bounds, boundaries = bounds)

        # Конвертация изображения в массив numpy.array
        fig = plt.gcf()
        fig.canvas.draw()
        image_array = np.array(fig.canvas.renderer.buffer_rgba())
        images.append(image_array)

        plt.close()


    # Сохраняем список изображений в виде гиф-изображения
    imageio.mimsave(output_file, images, duration=0.3)