import cython
import numpy as np
cimport numpy as cnp
cnp.import_array()
from cython.parallel import prange #параллельные циклы для тел


# Гравитационная постоянная
cdef double G = 6.6743e-11


# Вычисление ускорения
def get_a(cnp.ndarray[double, ndim=2] rv, cnp.ndarray[double, ndim=1] mass):
    cdef int i, j
    cdef int N = mass.shape[0]
    cdef cnp.ndarray[double, ndim=2] a = np.zeros((N, 3), dtype=np.float64)
    for i in range(N):
        for j in range(N):
            if j != i:
                r_diff = [rv[j, k] - rv[i, k] for k in range(3)]
                a[i, 0] += G * mass[j] * r_diff[0] / np.linalg.norm(r_diff)**3
                a[i, 1] += G * mass[j] * r_diff[1] / np.linalg.norm(r_diff)**3
                a[i, 2] += G * mass[j] * r_diff[2] / np.linalg.norm(r_diff)**3 
    return a



# Метод Верле
def solver4(cnp.ndarray[double, ndim = 1] mass, 
            cnp.ndarray[double, ndim = 2] rv_start,
            cnp.ndarray[double, ndim = 1] t):

    #rv_start = [[rx ry rz vx vy vz]     [rx ry rz vx vy vz]     ....  [rx ry rz vx vy vz]]
    cdef int N = mass.shape[0]
    cdef double dt = ((t[0] + t[-1]) / t.shape[0])
    cdef cnp.ndarray[double, ndim=3] res = np.empty((t.shape[0], N, 6), dtype=np.float64)

    cdef int i, j
    for i in range(N):
        res[0, i, :] = rv_start[i]


    # a(n) = dv(n)/dt
    cdef cnp.ndarray[double, ndim=2] a_n = get_a(rv_start, mass)
    cdef cnp.ndarray[double, ndim=2] a_n1
    
    for i in range(1, t.shape[0]):
        # r(n+1) = (rx, ry, rz)
        for j in prange(N, nogil=True):
            res[i, j, 0] = res[i - 1, j, 0] + dt * res[i - 1, j, 3] + 0.5 * a_n[j, 0] * dt**2
            res[i, j, 1] = res[i - 1, j, 1] + dt * res[i - 1, j, 4] + 0.5 * a_n[j, 1] * dt**2
            res[i, j, 2] = res[i - 1, j, 2] + dt * res[i - 1, j, 5] + 0.5 * a_n[j, 2] * dt**2

        #v(n + 1) = (vx, vy, vz)
        a_n1 = get_a(res[i, :, :], mass)
        for j in prange(N, nogil=True):
            res[i, j, 3] = res[i - 1, j, 3] + 0.5 * (a_n1[j, 0] + a_n[j, 0]) * dt
            res[i, j, 4] = res[i - 1, j, 4] + 0.5 * (a_n1[j, 1] + a_n[j, 1]) * dt
            res[i, j, 5] = res[i - 1, j, 5] + 0.5 * (a_n1[j, 2] + a_n[j, 2]) * dt
        
        a_n = a_n1
    return res