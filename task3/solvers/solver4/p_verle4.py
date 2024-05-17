import solvers.solver4.c_verle4 as ccode
import numpy as np
from numpy import ndarray

def solver4_py(mass: ndarray, rv_start: ndarray, t: ndarray) -> ndarray:
    return ccode.solver4(mass.astype(np.float64), rv_start.astype(np.float64), t.astype(np.float64))