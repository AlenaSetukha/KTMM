import numpy as np
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import fenics
import string

def plot_sol(mesh: fenics.Mesh, solution, title_str: string):
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