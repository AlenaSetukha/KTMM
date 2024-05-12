from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt


'''
def plot_3d_points(solution: ndarray) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = []
    y = []
    z = []

    for i in range(0, solution.shape[1], 6):
        x.append(solution[:, i])


    
    x = [r[0] for r in solution[:, i] for i in range(0, solution.shape[1], 6)]
    y = [r[1] for r in points]
    z = [r[2] for r in points]
    
    ax.scatter(x, y, z, c = 'r', marker='o')  # Рисуем точки в виде красных сфер
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.set_title('3D Points')
    
    plt.show()'''