import math
from Param import Param
from Mesh_Triangle import Mesh_Triangle
import numpy as np

from scipy.integrate import odeint
from scipy.optimize import fsolve


# Вспомогательные функции для коэффициента QR
@staticmethod
def zero_func(t: float, A: float) -> float:
    return 0.

@staticmethod
def sin_def_6(t: float, A: float) -> float:
    return A * (22 + 2 * math.sin(t / 6))

@staticmethod
def sin_def_8(t: float, A: float) -> float:
    return A * (22 + 2 * math.sin(t / 8))




class Ode_Solver:
    def __init__(self, mesh: Mesh_Triangle, param: Param):
        self.matrix_kij = np.zeros((mesh.num_elmnt, mesh.num_elmnt), dtype=float)
        self.mult_QE_vec = np.zeros(mesh.num_elmnt, dtype=float)
        for i in range(mesh.num_elmnt):
            for j in range(mesh.num_elmnt):
                self.matrix_kij[i][j] =  mesh.Sij[i][j] * param.lambda_ij[i][j]
            self.mult_QE_vec[i] = -5.67 * param.eps[i] * mesh.Si[i] / (100.**4)

        self.ci = param.c_coef

        self.QiR = [zero_func, sin_def_8, zero_func,
                    zero_func, zero_func, zero_func, 
                    zero_func, sin_def_6, zero_func]
        self.A_const = 1.


    # Получение правой части системы
    def get_right_side(self, y: np.ndarray, t: np.ndarray) -> np.ndarray:
        right_side = np.zeros(y.shape[0], dtype=float)

        for i in range(y.shape[0]):
            sum_j = 0.
            for j in range(y.shape[0]):
                sum_j += self.matrix_kij[i][j] * (y[j] - y[i])
            right_side[i] = (sum_j + self.mult_QE_vec[i] * (y[i]**4) + self.QiR[i](t, self.A_const)) / self.ci[i]
        return right_side
    

    # Получение правой части системы в стационарном случае
    def get_right_side_stationar(self, y: np.ndarray) -> np.ndarray:
        right_side = np.zeros(y.shape[0], dtype=float)

        for i in range(y.shape[0]):
            sum_j = 0.
            for j in range(y.shape[0]):
                sum_j += self.matrix_kij[i][j] * (y[j] - y[i])
            right_side[i] = (sum_j + self.mult_QE_vec[i] * (y[i]**4)) / self.ci[i]
        return right_side

        

    def ode_calculate_temp(self, param: Param) -> np.ndarray:
        system_sol = odeint(self.get_right_side, param.start_temp, param.time_grid)
        return system_sol
    

    def ode_calculate_temp_stationar(self, param: Param) -> np.ndarray:
        t0 = np.ones(param.num_elmnts, dtype=float) 
        system_sol_stationar = fsolve(self.get_right_side_stationar, t0)
        return system_sol_stationar