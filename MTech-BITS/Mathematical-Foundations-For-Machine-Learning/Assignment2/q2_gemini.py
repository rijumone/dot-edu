import numpy as np


def gradient(f, x):
  """
  Calculates the gradient of a function f at a point x.

  Args:
    f: The function to calculate the gradient of.
    x: A NumPy array representing the point (with two elements for x and y).

  Returns:
    A NumPy array representing the gradient of f at x.
  """
  h = 1e-5
  grad = np.zeros_like(x)
  # Used to store the gradient of a function, where each element corresponds to the partial derivative with respect to the corresponding element in x.
  for i in range(len(x)):
    dx = np.zeros_like(x)
    # This array dx is typically used to represent a small displacement or change in the values of x. 
    dx[i] = h
    grad[i] = (f(x + dx) - f(x - dx)) / (2 * h)
  return grad


def armijo_rule(f, grad, x, alpha):
  """
  Implements Armijo's rule to choose the step size alpha.

  Args:
    f: The function to minimize.
    grad: The gradient of the function.
    x: The current point.
    alpha: The initial step size.

  Returns:
    The new step size chosen by Armijo's rule.
  """
  c1 = 1e-4
  c2 = 0.5
  print(f"Initial alpha: {alpha}")
  while f(x - alpha * grad) > f(x) + c1 * alpha * np.dot(grad, grad):
    alpha *= c2
    print(f"Reduced alpha: {alpha}")

  return alpha


def gradient_descent(f, x0, alpha=0.1, tol=1e-6, max_iter=1000):
  """
  Performs gradient descent to find a stationary point of a function.

  Args:
    f: The function to minimize (with two variables).
    x0: The initial guess for the minimum (NumPy array with two elements).
    alpha: The initial step size.
    tol: The tolerance for convergence.
    max_iter: The maximum number of iterations.

  Returns:
    The minimum point found by gradient descent (NumPy array).
  """
  x = x0
  for _ in range(max_iter):
    print(f'\n=============\niteration {_+1} of {max_iter}')
    print('x:', x[0], 'y:', x[1])
    grad = gradient(f, x)
    alpha = armijo_rule(f, grad, x, alpha)
    print('alpha:', alpha)
    print('f(x, y)', f(x))
    x -= alpha * grad
    if np.linalg.norm(grad) < tol:
      break
  return x


def f(x):
  # return x[0]**2 + 2*x[0]*x[1] + x[1]**2
  return 10 * x[0]**4 - 20 * x[0]**2 * x[1] + x[0]**2 + 10 * x[1]**2 - 2 * x[0] + 1


x0 = np.array([1.0, 2.0])
x_min = gradient_descent(f, x0, max_iter=10)
print('\n=============\n')
print(f"Minimum point: {x_min}")
print(f"Function value at minimum: {f(x_min)}")
