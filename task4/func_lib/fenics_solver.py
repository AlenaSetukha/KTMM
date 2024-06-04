import fenics

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