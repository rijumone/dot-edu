"""
Q1) Finding solutions of linear systems
a) Write a code taking as input a matrix A of size m x n and a vector b of size m x 1, where m and n are arbitrarily large numbers and m < n, constructing the augmented matrix and performing
 REF, and  RREF
without using any built-in functions. In case you encounter any divi- sion by 0, you can choose a different A and/or b.
Deliverables: The code snippet showing the procedure for REF and RREF. (1 mark + 1 mark)
"""


import pdb


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


def is_ref(matrix: list) -> bool:
    """Given a matrix, determine if it is in RREF form.

    Args:
        augmented_matrix (list)

    Returns:
        bool
    """
    # First check:
    # If a row does not entirely consists of
    # zeros, than the first non zero number is 1.
    # import pdb;pdb.set_trace()
    # for row in matrix:
    #     print(row)
    
    # import pdb;pdb.set_trace()
    for row in matrix:
        check_one_passed = False
        if len(row) != len([_ for _ in row if int(_) == 0]):
            for element in row:
                if element in [0, 0.0, -0, -0.0]:
                    continue
                elif element in [1, 1.0]:
                    check_one_passed = True
                    break
                else:
                    check_one_passed = False
                    break

        if not check_one_passed:
            return False
    
    # Second check:
    # All zero rows should be on the bottom of the matrix
    idx_first_zero_row = -1
    for idx, row in enumerate(matrix):
        if len(row) == len([_ for _ in row if int(_) == 0]):
            idx_first_zero_row = idx
        else:
            if idx < idx_first_zero_row:
                return False
        
    # Third check:
    # In any two successive rows that do not consist entirely of zeroes,
    # the leading 1 in the lower row occcurs further to the right than the
    # leading 1 in the higher row.
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
    if is_ref(matrix):
        return matrix
    
    m = len(matrix)
    n = len(matrix[0])
    # Step 1: Locate the leftmost column that does not contain entirely of zeros.
    non_zero_column = 0
    for j in range(n):
        if len([matrix[i][j] for i in range(m) if matrix[i][j] == 0]) != m:
            non_zero_column = j
            break
    
    non_zero_row = 0
    # Step 2: interchange top row with a row w/ non zero element if needed
    if matrix[0][non_zero_column] == 0:
        # find non zero row
        non_zero_row = 1
        for i in range(1,m):
            if matrix[i][non_zero_column] != 0:
                non_zero_row = i
                break
    
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
    
    
    while not is_ref(matrix):
        print(f'matrix: {matrix}')
        matrix = [matrix[0]] + matrix_to_ref(matrix[1:])
    return matrix


def ref_to_rref(matrix: list) -> list:
    m = len(matrix)
    n = len(matrix[0])

    for row in range(m):
        leading_col = -1  # Track the column of the leading 1 in this row
        for column in range(n):
            if matrix[row][column] in [1, 1.0]:
                leading_col = column
                break

        if leading_col != -1:  # If a leading 1 is found
            # Make all other entries in other rows in the leading column as zero
            for i in range(m):
                if i != row and matrix[i][leading_col] not in [0, -0, 0.0, -0.0]:
                    # find multiplier
                    multiplier = matrix[i][leading_col]
                    for j in range(n):
                        matrix[i][j] -= multiplier * matrix[row][j]

    return matrix
    
def identify_pivot_non_pivot_cols(matrix: list) -> (list, list):
    """Given a matrix in its REF or RREF form, identify and return
    the indices of the pivot columns. Pivot columns are those which have
    a leading 1 in them, non pivot are the remaining columns.

    Args:
        matrix (list): list of lists of real numbers representing a matrix

    Returns:
        list, list: Tuple of lists of lists of real numbers representing a matrix
    """
    m = len(matrix)
    n = len(matrix[0])
    pivot_cols, non_pivot_cols = [], []
    for j in range(n):
        is_pivot = False
        for i in range(m):
            if matrix[i][j] == 1 and all(matrix[_][j] in [0, 0.0, -0, -0.0] for _ in range(i)):
                is_pivot = True
                break
        if is_pivot:    pivot_cols.append(j)
        else:   non_pivot_cols.append(j)
    return pivot_cols, non_pivot_cols

def main2():
    pivot_cols, non_pivot_cols = identify_pivot_non_pivot_cols([
        [1.0, 2.0, 0.0, 3.0, 0.0, 7.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 2.0]
    ])
    print(pivot_cols, non_pivot_cols)


def main1():
    print(is_ref([
        [1.0,   2.0,    -5.0,   3.0,    6.0,    14.0], 
        [0,     0,      -2,     0,      7,      12], 
        [0.0,   0.0,    5.0,    0.0,    -17.0,  -29.0],
    ]))
    print(is_ref([
        [-0.0, -0.0, 1.0, -0.0, -3.5, -6.0], 
        [0.0, 0.0, 0.0, 0.0, 0.5, 1.0],
    ]))


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

    is_ref_o = is_ref(matrix=augmented_matrix)
    print(is_ref_o)

    ref_matrix = matrix_to_ref(matrix=augmented_matrix)


    is_ref_o = is_ref(matrix=augmented_matrix)
    print(is_ref_o)

    print('REF')
    for row in ref_matrix:
        print(row)

    rref_matrix = ref_to_rref(ref_matrix)
    print('RREF')
    for row in rref_matrix:
        print(row)




if __name__ == '__main__':
    # main()
    # main1()
    main2()
