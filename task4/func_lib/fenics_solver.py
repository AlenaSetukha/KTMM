import fenics
import numpy as np
from typing import List

def fenics_solution(function_space: fenics.FunctionSpace, alpha: fenics.Constant,
                 f:fenics.Expression, h: fenics.Expression, g: fenics.Expression) -> fenics.Function:
    
    def boundary(x, on_boundary):
        return on_boundary
    boundary_conditions = fenics.DirichletBC(function_space, h, boundary)

    u = fenics.TrialFunction(function_space)
    v = fenics.TestFunction(function_space)
    
    # Define linear and bilinear form
    a = (fenics.dot(fenics.grad(u), fenics.grad(v)) + alpha * u * v) * fenics.dx
    L = f * v * fenics.dx + g * v * fenics.ds
    
    # Solve problem
    u_h = fenics.Function(function_space)
    fenics.solve(a == L, u_h, boundary_conditions)

    return u_h



def fenics_solution_t(function_space: fenics.FunctionSpace,
                      time_grid: np.ndarray, alpha: fenics.Constant,
                      f:fenics.Expression, h: fenics.Expression,
                      g: fenics.Expression, u0: fenics.Expression) -> List[fenics.Function]:
    
    dt = time_grid[1] - time_grid[0]
    #Делаем для u0 преобразование Expression в Function
    prev_U = fenics.interpolate(u0, function_space) #численное стратовое приближение
    result = [prev_U.copy()]

    #На каждом шагу решаем задачу
    for i in range(1, time_grid.shape[0]):
        t = time_grid[i]
        f.t = t
        h.t = t
        g.t = t
        num_sol = fenics_solution(function_space, 1 / (dt * alpha), prev_U / (dt * alpha) + f / alpha, h, g)

        prev_U.assign(num_sol)
        result.append(num_sol.copy())
    
    return result