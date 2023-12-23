"""
Q1) Finding solutions of linear systems
a) Write a code taking as input a matrix A of size m x n and a vector b of size m x 1, where m and n are arbitrarily large numbers and m < n, constructing the augmented matrix and performing
 REF, and  RREF
without using any built-in functions. In case you encounter any divi- sion by 0, you can choose a different A and/or b.
Deliverables: The code snippet showing the procedure for REF and RREF. (1 mark + 1 mark)
"""


def construct_augmented_matrix(A, B):
    if len(A) != len(B):
        raise ValueError(
            "Matrix A and vector B must have the same number of rows.")

    m, n = len(A), len(A[0])
    if m >= n:
        raise ValueError(
            "Number of rows in matrix A must be less than the number of columns.")

    augmented_matrix = []
    for i in range(m):
        row = A[i] + [B[i][0]]
        augmented_matrix.append(row)

    return augmented_matrix


def is_rref(matrix: list) -> bool:
    """Given a matrix, determine if it is in RREF form.

    Args:
        augmented_matrix (list)

    Returns:
        bool
    """
    # First check:
    # If a row does not entirely consists of
    # zeros, than the first non zero number is 1.
    import pdb;pdb.set_trace()
    for row in matrix:
        print(row)
    check_one_passed = False
    for row in matrix:
        if len(row) != len([_ for _ in row if int(_) == 0]):
            for element in row:
                if int(element) == 0:
                    continue
                elif int(element) == 1:
                    check_one_passed = True
                    break
    # Second check:
    # Third check:
    if not check_one_passed:
        return False
    last_lead_position = -1
    for row in matrix:
        for j in range(len(row)):
            if int(row[j]) == 1:
                if j < last_lead_position:
                    return False
                last_lead_position = j
    return True



def matrix_to_ref(matrix: list) -> list:
    """Given a matrix, convert it to one of its REF.

    Args:
        matrix (list): list of lists of real numbers representing a matrix

    Returns:
        list: list of lists of real numbers representing a matrix
    """
    import pdb;pdb.set_trace()
    m = len(matrix)
    n = len(matrix[0])

    # Step 1: Locate the leftmost column that does not contain entirely of zeros.
    non_zero_column = 0
    for j in range(n):
        if len([matrix[i][j] for i in range(m) if matrix[i][j] == 0]) != m:
            non_zero_column = j
            break
    
    # print(non_zero_column)
    non_zero_row = 0
    # Step 2: interchange top row with a row w/ non zero element if needed
    if matrix[0][non_zero_column] == 0:
        # find non zero row
        non_zero_row = 1
        for i in range(1,m):
            if matrix[i][non_zero_column] != 0:
                non_zero_row = i
                break
    
    # print(non_zero_row)
    matrix[0], matrix[non_zero_row] = matrix[non_zero_row], matrix[0]

    # Step 3: if the entry that is now at the top of the non_zero_column is a != 0,
    # multiple by 1/a, to let it become 1, in order to introduce a leading 1
    if matrix[0][non_zero_column] != 0:
        matrix[0] = [_*(1/matrix[0][non_zero_column]) for _ in matrix[0]]

    
    # Step 4: add suitable multiples of the top row to the bottom rows so that all
    # the entries below the leading 1 become 0
    for row in range(1, m):
        if matrix[row][non_zero_column] == 0:
            continue
        # find multiplier
        multiplier = matrix[row][non_zero_column] / matrix[0][non_zero_column] * -1
        for j in range(n):
            matrix[row][j] += multiplier * matrix[0][j]
    
    while not is_rref(matrix):
        print(f'matrix: {matrix}')
        matrix = matrix[0] + matrix_to_ref(matrix[1:])
    return matrix


    

def main1():
    print(is_rref([[0.0, 0.0, 0.0, 0.0, 1.0, 2.0]]))


def main():
    # Example usage:
    # Define matrix A and vector B
    matrix_A = [[0, 0, -2, 0, 7],
                [2, 4, -10, 6, 12],
                [2, 4, -5, 6, -5]]
    vector_B = [[12],
                [28],
                [-1]]

    # Construct the augmented matrix
    augmented_matrix = construct_augmented_matrix(matrix_A, vector_B)
    print("Augmented matrix:")
    for row in augmented_matrix:
        print(row)

    is_rref_o = is_rref(matrix=augmented_matrix)
    print(is_rref_o)

    ref_matrix = matrix_to_ref(matrix=augmented_matrix)

    print('main')
    for row in ref_matrix:
        print(row)



if __name__ == '__main__':
    main()
    # main1()
