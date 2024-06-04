import fenics
import numpy as np

def get_errors(u_exact: fenics.Expression, num_sol: fenics.Expression, mesh: fenics.Mesh):
    # L2 
    error_L2 = fenics.errornorm(u_exact, num_sol, 'L2')
    # MAX 
    u_exact_vertex_vals = u_exact.compute_vertex_values(mesh)
    u_h_vertex_vals = num_sol.compute_vertex_values(mesh)
    error_max = np.max(np.abs(u_exact_vertex_vals - u_h_vertex_vals))

    return error_L2, error_max