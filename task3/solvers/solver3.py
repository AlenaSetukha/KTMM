import math
import numpy as np
from numpy import ndarray
import multiprocessing as mp
from multiprocessing.pool import Pool

# Гравитационная постоянная
G = 6.6743e-11


# Функция вычисления ускорения для одного тела
def get_a_mltp(args: tuple) -> ndarray: 
    mass = args[0]
    r = args[1]
    i = args[2]
    # ax ay az
    a = np.zeros(3, dtype= np.float64)
    for j in range(mass.shape[0]):
        if j != i:
            r_diff = [r[j][k] - r[i][k] for k in range(3)]
            a[0] += G * mass[j] * r_diff[0] / np.linalg.norm(r_diff)**3
            a[1] += G * mass[j] * r_diff[1] / np.linalg.norm(r_diff)**3
            a[2] += G * mass[j] * r_diff[2] / np.linalg.norm(r_diff)**3
    return a


# Функция вычисления ускорения
def get_a(p: Pool, r: ndarray, mass: ndarray) -> ndarray:
    a = p.map(get_a_mltp, [(mass, r, i) for i in range(mass.shape[0])])
    return np.array(a)




# Функция расчета x_n+1 для одного тела
def get_r_mltp(args: tuple) -> ndarray:
    rv = args[0]
    a_n = args[1]
    dt = args[2]
    r = [rv[0] + rv[3] * dt + 0.5 * a_n[0] * dt**2,
         rv[1] + rv[4] * dt + 0.5 * a_n[1] * dt**2,
         rv[2] + rv[5] * dt + 0.5 * a_n[2] * dt**2]
    return np.array(r)


# Функция расчета v_n+1 для одного тела
def get_v_mltp(args: tuple) -> ndarray:
    rv = args[0]
    a_n = args[1]
    a_n1 = args[2]
    dt = args[3]
    v = [rv[3] + 0.5 * (a_n[0] + a_n1[0]) * dt,
         rv[4] + 0.5 * (a_n[1] + a_n1[1]) * dt,
         rv[5] + 0.5 * (a_n[2] + a_n1[2]) * dt]
    return np.array(v)   




def solver3(mass: ndarray, rv_start: ndarray, t: ndarray) -> ndarray:
    #rv_start = [[rx ry rz vx vy vz]   [rx ry rz vx vy vz]  ....  [rx ry rz vx vy vz]]
    N = mass.shape[0]
    res = np.empty((t.shape[0], N, 6), dtype=np.float64)
    for i in range(N):
        res[0, i, :] = rv_start[i]

    dt = ((t[0] + t[-1]) / t.shape[0]).astype(np.float64)

    p = mp.Pool(mp.cpu_count()) # параллелим тела


    # a(n) = dv(n)/dt
    r_start = [] #[[] [] [] ... []] - ndarray
    for item in rv_start:
        rx, ry, rz, *_ = item  # Используем звёздочку для распаковки оставшихся координат
        r_start.append(np.array([rx, ry, rz]))
    r_start = np.array(r_start)

    a_n = get_a(p, r_start, mass)

    for i in range(1, t.shape[0]):
        # r(n+1) = (rx, ry, rz)
        r_next = p.map(get_r_mltp, [(res[i - 1, j, :], a_n[j], dt) for j in range(N)])
        r_next = np.array(r_next)

        #v(n + 1) = (vx, vy, vz)
        a_n1 = get_a(p, r_next, mass)
        v_next = p.map(get_v_mltp, [(res[i - 1, j, :], a_n[j], a_n1[j], dt) for j in range(N)])

        # Сборка результата
        for j in range(N):
            res[i, j, :] = np.concatenate((r_next[j], v_next[j]), axis=0)
    
        a_n = a_n1
    
    return res
    

