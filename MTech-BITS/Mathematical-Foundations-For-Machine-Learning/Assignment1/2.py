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


def main():
    matrix_A = [
        [4, 3, -2],
        [8, 5, 2],
        [4, 6, 5]
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


if __name__ == '__main__':
    main()
