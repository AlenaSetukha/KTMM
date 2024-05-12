import math
import numpy as np
from numpy import ndarray
from scipy.integrate import odeint


# Гравитационная постоянная
G = 6.6743e-11

class Ode_Solver:
    def __init__(self, mass: ndarray):
        self.mass = mass
        self.N = mass.shape[0]


    # Получение правой части системы
    def get_right_side(self, y: ndarray, t: ndarray) -> ndarray:
        res = np.zeros(y.shape[0])

        #vi
        for i in range(self.N):
            res[i * 6] = y[i * 6 + 3]
            res[i * 6 + 1] = y[i * 6 + 4]
            res[i * 6 + 2] = y[i * 6 + 5]

        #sum
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    r_diff = [y[j * 6 + k] - y[i * 6 + k] for k in range(3)]
                    res[i * 6 + 3] += G * self.mass[j] * r_diff[0] / np.linalg.norm(r_diff)**3
                    res[i * 6 + 4]  += G * self.mass[j] * r_diff[1] / np.linalg.norm(r_diff)**3
                    res[i * 6 + 5]  += G * self.mass[j] * r_diff[2] / np.linalg.norm(r_diff)**3
        return res
    

def solver1(mass: ndarray, rv_start: ndarray, time_grid: ndarray) ->  ndarray:
    solver = Ode_Solver(mass)
    system_sol = odeint(solver.get_right_side, rv_start, time_grid)
    return system_sol
    
    
