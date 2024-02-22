def dot_product(vec1, vec2):
    """Calculate the dot product of two vectors."""
    return sum(a * b for a, b in zip(vec1, vec2))

def armijo_rule(func, grad, x, alpha, c, max_iter=1000, tol=1e-6):
    """
    Armijo's rule for choosing step size alpha.

    Parameters:
    func : callable
        Objective function.
    grad : callable
        Gradient of the objective function.
    x : list
        Current point.
    alpha : float
        Initial step size.
    c : float
        Armijo constant (sufficient decrease parameter).
    max_iter : int, optional
        Maximum number of iterations (default is 1000).
    tol : float, optional
        Tolerance for stopping criterion (default is 1e-6).

    Returns:
    float
        Chosen step size alpha.
    """
    while max_iter > 0:
        if func([x[i] - alpha * grad(x)[i] for i in range(len(x))]) <= func(x) + c * alpha * dot_product(grad(x), grad(x)):
            return alpha
        else:
            alpha *= 0.5
            max_iter -= 1
    return alpha

def gradient_descent(func, grad, initial_point, alpha_init=1.0, c=0.5, max_iter=1000, tol=1e-6):
    """
    Gradient descent with Armijo's rule for step size selection.

    Parameters:
    func : callable
        Objective function.
    grad : callable
        Gradient of the objective function.
    initial_point : list
        Initial point for optimization.
    alpha_init : float, optional
        Initial step size (default is 1.0).
    c : float, optional
        Armijo constant (sufficient decrease parameter) for Armijo's rule (default is 0.5).
    max_iter : int, optional
        Maximum number of iterations (default is 1000).
    tol : float, optional
        Tolerance for stopping criterion (default is 1e-6).

    Returns:
    list
        Optimal point (stationary point).
    """
    x = initial_point[:]
    alpha = alpha_init
    iter_count = 0
    while iter_count < max_iter:
        gradient = grad(x)
        alpha = armijo_rule(func, grad, x, alpha, c)
        x = [x[i] - alpha * gradient[i] for i in range(len(x))]
        if sum(g ** 2 for g in gradient) < tol:
            break
        iter_count += 1
    return x

# Example usage:
if __name__ == "__main__":
    # Define the mathematical function and its gradient
    def function(x):
        return 10 * x[0]**4 - 20 * x[0]**2 * x[1] + x[0]**2 + 10 * x[1]**2 - 2 * x[0] + 1


    def gradient(x):
        return [40 * x[0]**3 - 40 * x[0] * x[1] + 2 * x[0] - 2,
                -20 * x[0]**2 + 20 * x[1]]

    # Initial point for optimization
    initial_point = [0.5, 0.5]

    # Perform gradient descent with Armijo's rule
    optimal_point = gradient_descent(function, gradient, initial_point)

    print("Optimal point (stationary point):", optimal_point)
    print("Function value at optimal point:", function(optimal_point))
