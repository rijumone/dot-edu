import random
import numpy as np


def lu_decomposition(matrix):
    n = len(matrix)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    # Initialize L as an identity matrix
    for i in range(n):
        L[i][i] = 1.0

    for i in range(n):
        print('=======')
        for row in U:
            print(row)
        print('=======')
        for row in L:
            print(row)
        # Upper Triangular Matrix
        for k in range(i, n):
            sum_ = 0
            for j in range(i):
                sum_ += L[i][j] * U[j][k]
            U[i][k] = matrix[i][k] - sum_

        # Lower Triangular Matrix
        for k in range(i, n):
            if i == k:
                L[i][i] = 1.0  # Diagonal of L is 1
            else:
                sum_ = 0
                for j in range(i):
                    sum_ += L[k][j] * U[j][i]
                L[k][i] = (matrix[k][i] - sum_) / U[i][i]

    return L, U


def cholesky_decomposition(matrix):
    n = len(matrix)
    L = np.zeros((n, n))

    for i in range(n):
        for j in range(i+1):
            if i == j:
                L[i][j] = np.sqrt(matrix[i][i] - sum(L[i][k] ** 2 for k in range(j)))
            else:
                L[i][j] = (1.0 / L[j][j] * (matrix[i][j] - sum(L[i][k] * L[j][k] for k in range(j))))

    return L


def dot_product(vec1, vec2):
    return sum(x * y for x, y in zip(vec1, vec2))

def norm(vector):
    return sum(x ** 2 for x in vector) ** 0.5

def generate_random_matrix(rows, cols):
    return [[round(random.uniform(-999.9, 999.9), 4) for _ in range(cols)] for _ in range(rows)]

def gram_schmidt_qr_decomposition(matrix):
    m, n = len(matrix), len(matrix[0])
    Q = [[0.0] * n for _ in range(m)]
    R = [[0.0] * n for _ in range(n)]

    for j in range(n):
        v = matrix[j]
        for i in range(j):
            R[i][j] = dot_product(Q[i], matrix[j])
            v = [x - R[i][j] * q for x, q in zip(v, Q[i])]

        R[j][j] = norm(v)
        Q[j] = [x / R[j][j] for x in v]

    return Q, R


def main():
    matrix_A = [
        [5, 1, 2],
        [1, 6, 3],
        [2, 3, 7]
    ]

    # Perform LU decomposition
    L_result, U_result = lu_decomposition(matrix_A)

    # Display the Lower and Upper triangular matrices L and U
    print("Lower Triangular Matrix L:")
    for row in L_result:
        print(row)

    print("\nUpper Triangular Matrix U:")
    for row in U_result:
        print(row)

    # Extract L and U from the LU decomposition
    A = np.array(matrix_A)
    L = np.array(L_result)
    U = np.array(U_result)

    # Multiply L and U matrices
    LU = np.dot(L, U)

    # Check if LU equals the original matrix A
    if np.array_equal(A, LU):
        print("LU decomposition is correct: A = LU")
    else:
        print("LU decomposition is incorrect: A != LU")

    # Compute Cholesky decomposition
    L_result = cholesky_decomposition(matrix_A)
    print("Lower Triangular Matrix L (Cholesky Decomposition):")
    print(L_result)

    # Verify A = LL^T
    verification_result = np.allclose(matrix_A, np.dot(L_result, np.transpose(L_result)))
    if verification_result:
        print("\nVerification: A = LL^T (Cholesky Decomposition is Correct)")
    else:
        print("\nVerification: A != LL^T (Cholesky Decomposition is Incorrect)")


    # Generate a randomly populated matrix with real numbers up to 4 digits in length
    matrix_A = generate_random_matrix(5, 4)

    # Perform Gram-Schmidt QR decomposition
    Q_result, R_result = gram_schmidt_qr_decomposition(matrix_A)

    # Display the matrices Q and R
    print("Matrix Q (Gram-Schmidt orthogonalization):")
    for row in Q_result:
        print(row)

    print("\nMatrix R (Upper triangular matrix):")
    for row in R_result:
        print(row)


if __name__ == '__main__':
    main()
