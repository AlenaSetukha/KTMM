import numpy as np
from numpy import ndarray

import matplotlib.pyplot as plt

def plot_xy(solution: ndarray, xylim: float, style: tuple[tuple[str,str,float]]) -> None:
    # Init plot
    fig = plt.figure(figsize=(10, 10))
    subplot = fig.add_subplot()
    
    # Set Ox, Oy limits
    subplot.set_xlim([-xylim, xylim])
    subplot.set_ylim([-xylim, xylim])
    
    # Plot planets
    scat_plots = []

    for i in range(0, solution.shape[1], 6):
        scat_plots.append(subplot.scatter(solution[:, i], solution[:, i + 1],
                        label=style[i//6][0], color=style[i//6][1], s=style[i//6][2] * 20))
    
    # Show legend
    subplot.legend()


def plot_xy_array(solution: ndarray, xylim: float, style: tuple[tuple[str,str,float]]) -> None:
    # Init plot
    fig = plt.figure(figsize=(10, 10))
    subplot = fig.add_subplot()
    
    # Set Ox, Oy limits
    subplot.set_xlim([-xylim, xylim])
    subplot.set_ylim([-xylim, xylim])
    
    # Plot planets
    scat_plots = []

    for i in range(0, solution.shape[1]):# рисую rx, ry
        scat_plots.append(subplot.scatter(solution[:, i, 0], solution[:, i, 1],
                        label=style[i][0], color=style[i][1], s=style[i][2] * 20))
    
    # Show legend
    subplot.legend()

