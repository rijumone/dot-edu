"""
Q1) Power Method and Associated problems (2 marks)

i) Generate using code a random integer matrix C of size 4×3 and a ma- trix A1 defined as A1 = CT C and workout its characteristic equation. Using any software package, determine the eigenvalues and eigenvec- tors.

Deliverables: The matrices C and A1, the computation of the characteristic equation, the eigenvalues and eigenvectors as obtained from the package.
"""

import random
import numpy as np


def generate_random_integer_matrix(m, n, min_value=0, max_value=10):
    """
    Generate a random integer matrix of size m x n with values between min_value and max_value.
    
    Parameters:
        m (int): Number of rows.
        n (int): Number of columns.
        min_value (int): Minimum value for random integers (inclusive). Default is 0.
        max_value (int): Maximum value for random integers (exclusive). Default is 10.
    
    Returns:
        list of lists: Random integer matrix of size m x n.
    """
    matrix = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append(random.randint(min_value, max_value - 1))
        matrix.append(row)
    return matrix

def transpose_matrix(matrix):
    """
    Compute the transpose of a matrix.
    
    Parameters:
        matrix (list of lists): Input matrix.
    
    Returns:
        list of lists: Transpose of the input matrix.
    """
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    
    # Initialize an empty matrix for the transpose
    transpose = [[0 for _ in range(num_rows)] for _ in range(num_cols)]
    
    # Compute the transpose
    for i in range(num_rows):
        for j in range(num_cols):
            transpose[j][i] = matrix[i][j]
    
    return transpose

def multiply_matrices(matrix_A, matrix_B):
    """
    Multiply two matrices.
    
    Parameters:
        matrix_A (list of lists): First matrix.
        matrix_B (list of lists): Second matrix.
    
    Returns:
        list of lists: Product of the two matrices.
    """
    # Check if dimensions are compatible for matrix multiplication
    if len(matrix_A[0]) != len(matrix_B):
        raise ValueError("Number of columns in matrix A must be equal to the number of rows in matrix B.")
    
    # Initialize an empty result matrix
    result = [[0 for _ in range(len(matrix_B[0]))] for _ in range(len(matrix_A))]
    
    # Perform matrix multiplication
    for i in range(len(matrix_A)):
        for j in range(len(matrix_B[0])):
            for k in range(len(matrix_B)):
                result[i][j] += matrix_A[i][k] * matrix_B[k][j]
    
    return result
      
def normalize_eigenvectors(eigenvalues, eigenvectors):
    """
    Normalize eigenvectors such that one of the values is 1.
    
    Parameters:
        eigenvalues (numpy.ndarray): Eigenvalues.
        eigenvectors (numpy.ndarray): Eigenvectors.
    
    Returns:
        numpy.ndarray: Normalized eigenvectors.
    """
    # Find the index of the eigenvalue corresponding to the largest magnitude
    index_max_magnitude = np.argmax(np.abs(eigenvalues))
    
    # Normalize the corresponding eigenvector to have a value of 1
    normalized_eigenvectors = eigenvectors / eigenvectors[index_max_magnitude]
    
    return normalized_eigenvectors

def characteristic_equation(matrix_A):
    """
    Compute the characteristic equation of a square matrix A.
    
    Parameters:
        matrix_A (numpy.ndarray): Square matrix.
    
    Returns:
        numpy.poly1d: Characteristic polynomial (equation) as a polynomial object.
    """
    # Check if matrix_A is square
    if matrix_A.shape[0] != matrix_A.shape[1]:
        raise ValueError("Input matrix must be square.")
    
    # Identity matrix of the same size as matrix_A
    identity = np.eye(matrix_A.shape[0])
    
    # Compute the characteristic polynomial
    characteristic_poly = np.poly(matrix_A - identity)
    return characteristic_poly

def matrix_vector_product(matrix, vector):
    """
    Compute the product of a matrix and a vector.

    Parameters:
        matrix (list of lists): Matrix.
        vector (list): Vector.

    Returns:
        list: Product of the matrix and the vector.
    """
    product = []
    for row in matrix:
        row_product = sum(row[i] * vector[i] for i in range(len(vector)))
        product.append(row_product)
    return product

def normalize_vector(vector):
    """
    Normalize a vector.

    Parameters:
        vector (list): Input vector.

    Returns:
        list: Normalized vector.
    """
    norm = sum(x ** 2 for x in vector) ** 0.5
    normalized_vector = [round((x / norm), 5) for x in vector]
    return normalized_vector

def normalize_vector_with_fixed_value(vector, fixed_index=0):
    """
    Normalize a vector such that one of its values is fixed at 1.

    Parameters:
        vector (list): Input vector.
        fixed_index (int): Index of the value that should be fixed at 1. Default is 0.

    Returns:
        list: Normalized vector with the specified value fixed at 1.
    """
    # Copy the input vector to avoid modifying the original vector
    normalized_vector = vector.copy()
    
    # Compute the magnitude (length) of the vector
    norm = sum(x ** 2 for x in normalized_vector) ** 0.5
    
    # Normalize the vector by dividing each component by the magnitude
    normalized_vector = [x / norm for x in normalized_vector]
    
    # Set the value at the fixed index to 1
    normalized_vector[fixed_index] = 1
    
    return normalized_vector

def power_method(matrix, max_iterations=100, tolerance=1e-9):
    """
    Power Method for finding the dominant eigenvalue and eigenvector of a matrix.

    Parameters:
        matrix (list of lists): Input matrix.
        max_iterations (int): Maximum number of iterations. Default is 100.
        tolerance (float): Tolerance for convergence. Default is 1e-6.

    Returns:
        float: Dominant eigenvalue.
        list: Dominant eigenvector.
    """
    n = len(matrix)
    
    # Initialize a random initial guess for the eigenvector
    eigenvector = [1] * n
    print('initial assumed eigenvector:', eigenvector)
    
    for _ in range(max_iterations):
        print(f'======\niteration: {_+1} of {max_iterations}')
        # Compute the matrix-vector product
        matrix_times_eigenvector = matrix_vector_product(matrix, eigenvector)
        
        # Normalize the resulting vector
        print(f'matrix_times_eigenvector: {matrix_times_eigenvector}')
        new_eigenvalue = max(matrix_times_eigenvector)
        print('new_eigenvalue:', new_eigenvalue)
        # new_eigenvector = normalize_vector(matrix_times_eigenvector)
        # new_eigenvector = normalize_vector_with_fixed_value(matrix_times_eigenvector)
        new_eigenvector = [round(_/new_eigenvalue, 4) for _ in matrix_times_eigenvector]
        print('new_eigenvector:', new_eigenvector)
        
        # Check for convergence
        if all(abs(new_eigenvector[i] - eigenvector[i]) < tolerance for i in range(n)):
            print('Convergence achieved')
            break
        
        eigenvector = new_eigenvector
    
    # Compute the dominant eigenvalue
    dominant_eigenvalue = sum(matrix_times_eigenvector[i] / eigenvector[i] for i in range(n)) / n
    
    return dominant_eigenvalue, eigenvector


def multiply_vector_with_transpose(vector):
    """
    Multiply a one-dimensional matrix (vector) with its transpose.

    Parameters:
        vector (list): Input vector.

    Returns:
        list of lists: Resultant matrix.
    """
    result_matrix = [[x * y for x in vector] for y in vector]
    return result_matrix

def subtract_matrices(matrix_A, matrix_B):
    """
    Subtract matrix B from matrix A.

    Parameters:
        matrix_A (list of lists): First matrix.
        matrix_B (list of lists): Second matrix.

    Returns:
        list of lists: Resultant matrix.
    """
    # Check if both matrices have the same dimensions
    if len(matrix_A) != len(matrix_B) or len(matrix_A[0]) != len(matrix_B[0]):
        raise ValueError("Matrices must have the same dimensions for subtraction.")
    
    # Subtract corresponding elements of the matrices
    result_matrix = [[matrix_A[i][j] - matrix_B[i][j] for j in range(len(matrix_A[0]))] for i in range(len(matrix_A))]
    
    return result_matrix

def main():
    # Example usage:
    m = 3
    n = 2

    print('\n+-------+')
    print('| Q-1-i |')
    print('+-------+\n')
    C = generate_random_integer_matrix(m, n, min_value=1, max_value=9)
    C = [
        [0, 1],
        [1, 1],
    ]
    print("Random Integer Matrix:")
    for row in C:
        print(row)

    CT = transpose_matrix(C)
    print("\nTransposed Matrix:")
    for row in CT:
        print(row)

    A1 = multiply_matrices(CT, C)

    print("A1:")
    for row in A1:
        print(row)

    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(np.array(A1))

    eigenvectors = normalize_eigenvectors(eigenvalues, eigenvectors)

    

    # Print the eigenvalues
    print("\nEigenvalues:")
    print([round(_, 5) for _ in eigenvalues])

    # Print the eigenvectors
    print("\nEigenvectors:")
    print(eigenvectors)
    
    c_e = characteristic_equation(np.array(A1))
    # Print the characteristic_equation
    print("\ncharacteristic_equation:")
    print(c_e)
    
    print('\n+--------+')
    print('| Q-1-ii |')
    print('+--------+\n')
    # A = [
    #     [0, 1], 
    #     [1, 1]
    # ]  # Example matrix

    dominant_eigenvalue, dominant_eigenvector = power_method(
        A1, max_iterations=10)
    print("Dominant Eigenvalue:", dominant_eigenvalue)
    print("Dominant Eigenvector:", dominant_eigenvector)
    x_1_hat = normalize_vector(dominant_eigenvector)
    print('x_1_hat', x_1_hat)
    # import pdb;pdb.set_trace()
    # x_1_hat_t = transpose_matrix([x_1_hat])
    
    print('\n+---------+')
    print('| Q-1-iii |')
    print('+---------+\n')
    # import pdb;pdb.set_trace()
    A2 = subtract_matrices(A1, multiply_matrices(A1, multiply_vector_with_transpose(x_1_hat)))
    print('A2', A2)
    dominant_eigenvalue, dominant_eigenvector = power_method(
        A2, max_iterations=10)
    print("Dominant Eigenvalue:", dominant_eigenvalue)
    print("Dominant Eigenvector:", dominant_eigenvector)
    x_2_hat = normalize_vector(dominant_eigenvector)
    print('x_2_hat', x_2_hat)
    
    print('\n+--------+')
    print('| Q-1-iv |')
    print('+--------+\n')

    A3 = subtract_matrices(A1,subtract_matrices(A1, multiply_matrices(A1, multiply_vector_with_transpose(x_1_hat))))
    print('A3', A3)
    dominant_eigenvalue, dominant_eigenvector = power_method(
        A3, max_iterations=10)
    print("Dominant Eigenvalue:", dominant_eigenvalue)
    print("Dominant Eigenvector:", dominant_eigenvector)
    x_3_hat = normalize_vector(dominant_eigenvector)
    print('x_3_hat', x_3_hat)
    


if __name__ == '__main__':
    main()
