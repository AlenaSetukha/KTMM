import numpy as np
from numpy import ndarray

# Гравитационная постоянная
G = 6.6743e-11

# Вычисление ускорения
def get_a(rv: ndarray, mass: ndarray) -> ndarray:
    a = np.zeros((mass.shape[0], 3), dtype=np.float64)
    for i in range(mass.shape[0]):
        for j in range(mass.shape[0]):
            if j != i:
                r_diff = [rv[j * 6 + k] - rv[i * 6 + k] for k in range(3)]
                a[i, 0] += G * mass[j] * r_diff[0] / np.linalg.norm(r_diff)**3
                a[i, 1] += G * mass[j] * r_diff[1] / np.linalg.norm(r_diff)**3
                a[i, 2] += G * mass[j] * r_diff[2] / np.linalg.norm(r_diff)**3 
    return a


# Метод Верле
def solver2(mass: ndarray, rv_start: ndarray, t: ndarray) -> ndarray:
    #[(rx ry rz vx vy vz)     (rx ry rz vx vy vz)     ....  (rx ry rz vx vy vz)]
    res = np.empty((t.shape[0], 3 * 2 * mass.shape[0]), dtype=np.float64)
    res[0, :] = rv_start
    dt = ((t[0] + t[-1]) / t.shape[0]).astype(np.float64)

    # a(n) = dv(n)/dt
    a_n = get_a(rv_start, mass)
    
    for i in range(1, t.shape[0]):
        # r(n+1) = (rx, ry, rz)
        for j in range (mass.shape[0]):
            res[i, j * 6] = res[i - 1, j * 6] + dt * res[i - 1, j * 6 + 3] + 0.5 * a_n[j, 0] * dt**2
            res[i, j * 6 + 1] = res[i - 1, j * 6 + 1] + dt * res[i - 1, j * 6 + 4] + 0.5 * a_n[j, 1] * dt**2
            res[i, j * 6 + 2] = res[i - 1, j * 6 + 2] + dt * res[i - 1, j * 6 + 5] + 0.5 * a_n[j, 2] * dt**2

        #v(n + 1) = (vx, vy, vz)
        a_n1 = get_a(res[i, :], mass)
        for j in range(mass.shape[0]):
            res[i, j * 6 + 3] = res[i - 1, j * 6 + 3] + 0.5 * (a_n1[j, 0] + a_n[j, 0]) * dt
            res[i, j * 6 + 4] = res[i - 1, j * 6 + 4] + 0.5 * (a_n1[j, 1] + a_n[j, 1]) * dt
            res[i, j * 6 + 5] = res[i - 1, j * 6 + 5] + 0.5 * (a_n1[j, 2] + a_n[j, 2]) * dt
        
        a_n = a_n1
    
    return res
