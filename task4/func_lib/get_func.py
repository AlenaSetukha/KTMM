import fenics
import numpy as np
from typing import List

def  get_func_list_from_expr(u_exact: fenics.Expression,
                time_grid: np.ndarray, function_space: fenics.FunctionSpace) -> List[fenics.Function]:
    res = []
    for i in range(time_grid.shape[0]):
        u_exact.t = time_grid[i]
        discrete_u = fenics.interpolate(u_exact, function_space)
        res.append(discrete_u)

    return res


def  get_list_of_expr(u_exact: fenics.Expression,
                time_grid: np.ndarray) -> List[fenics.Expression]:
    res = []
    for i in range(time_grid.shape[0]):
        u_exact.t = time_grid[i]
        res.append(u_exact)

    return res