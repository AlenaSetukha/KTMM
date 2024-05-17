import numpy as np
from numpy import ndarray
from typing import Tuple
import time
from solvers.solver2 import solver2
from solvers.solver3 import solver3
from solvers.solver4.p_verle4 import solver4_py


def get_random_rvm(N: int) -> Tuple[ndarray, ndarray]:
    rv = np.random.randint(50 * 10**9, 45000 * 10**9, N * 6)
    mass = np.random.randint(10**9, 10**10, N)
    return rv, mass

def get_random_rv_array(N: int) -> ndarray:
    rv = np.random.randint(50 * 10**9, 45000 * 10**9, (N, 6))
    return rv





def get_exc_time(rv_start: ndarray,
                 rv_start_array: ndarray,
                 mass: ndarray,
                 time_grid: ndarray,
                 N: int) -> Tuple[float, float, float]:
    # solver2
    start_time = time.time()
    solve2 = solver2(mass, rv_start, time_grid)
    end_time = time.time()
    t1 = end_time - start_time

    # solver3
    start_time = time.time()
    solve3 = solver3(mass, rv_start_array, time_grid)
    end_time = time.time()
    t2 = end_time - start_time

    # solver4
    start_time = time.time()
    solve4 = solver4_py(mass, rv_start_array, time_grid)
    end_time = time.time()
    t3 = end_time - start_time

    return t1, t2, t3
    
