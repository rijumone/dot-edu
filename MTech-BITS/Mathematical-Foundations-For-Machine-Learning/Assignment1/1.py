"""
Q1) Finding solutions of linear systems
a) Write a code taking as input a matrix A of size m x n and a vector b of size m x 1, where m and n are arbitrarily large numbers and m < n, constructing the augmented matrix and performing
 REF, and  RREF
without using any built-in functions. In case you encounter any divi- sion by 0, you can choose a different A and/or b.
Deliverables: The code snippet showing the procedure for REF and RREF. (1 mark + 1 mark)
"""


from random import randint, uniform
import numpy as np


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
        row = A[i] + [B[i][0] * -1]
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
    for row in matrix:
        check_one_passed = False
        if len(row) != len([_ for _ in row if int(_) in [0, -0, 0.0, -0.0]]):
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
        if len(row) == len([_ for _ in row if int(_) in [0, -0, 0.0, -0.0]]):
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
        if len([matrix[i][j] for i in range(m) if matrix[i][j] in [0, -0, 0.0, -0.0]]) != m:
            non_zero_column = j
            break
    
    non_zero_row = 0
    
    # Step 2: interchange top row with a row w/ non zero element if needed
    if matrix[0][non_zero_column] in [0, -0, 0.0, -0.0]:
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
        if matrix[row][non_zero_column] in [0, -0, 0.0, -0.0]:
            continue
        # find multiplier
        multiplier = matrix[row][non_zero_column] / matrix[0][non_zero_column] * -1
        for j in range(n):
            matrix[row][j] += multiplier * matrix[0][j]
    
    # Step 5: now first row is done, assume that it does not exist and repeat steps
    # 1 through 4 for the remaining rows.
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


def calculate_particular_solution(rref_matrix, pivot_indices):
    particular_solution = [0] * len(rref_matrix[0])

    # Create the particular solution using values from the RREF matrix
    for idx, pivot_col in enumerate(pivot_indices):
        if pivot_col < len(rref_matrix):
            particular_solution[pivot_col] = rref_matrix[idx][-1]

    return particular_solution


def calculate_homogeneous_solutions(rref_matrix, pivot_indices):
    num_variables = len(rref_matrix[0])
    num_equations = len(rref_matrix)
    
    # Determine the free variables
    free_variables = [col for col in range(num_variables) if col not in pivot_indices]

    # Initialize solutions
    solutions = []

    for _ in range(len(free_variables)):
        solution = [0] * num_variables
        for pivot_idx in pivot_indices:
            if pivot_idx < num_equations:  # Check if pivot_idx is within the bounds
                solution[pivot_idx] = rref_matrix[pivot_idx][free_variables[_]]
        solution[free_variables[_]] = 1
        solutions.append(solution)

    return solutions


def find_nullspace_solutions(rref_matrix, pivot_indices):
    num_variables = len(rref_matrix[0])
    pivot_set = set(pivot_indices)
    free_variables = [i for i in range(num_variables) if i not in pivot_set]

    solutions = []
    for free_var in free_variables:
        solution = [0] * num_variables
        solution[free_var] = 1  # Setting the free variable as 1
        
        for pivot_col, row_idx in zip(pivot_indices, range(len(rref_matrix))):
            coefficient = -rref_matrix[row_idx][free_var]
            if pivot_col < free_var:
                solution[pivot_col] = coefficient
            elif pivot_col > free_var:
                solution[pivot_col] = coefficient
                break  # We've covered all relevant rows for this variable

        solutions.append(solution)

    return solutions

def validate_homogeneous_solutions(rref_matrix, solutions, tolerance=1e-10):
    A = np.array(rref_matrix)
    validated_solutions = []

    for sol in solutions:
        x = np.array(sol)
        Ax = np.dot(A, x)
        
        # Check if Ax is approximately zero
        import pdb;pdb.set_trace()
        if np.allclose(Ax, np.zeros_like(Ax), atol=tolerance):
            validated_solutions.append(sol)

    return validated_solutions

def general_solution_from_rref(rref_matrix, pivot_indices):
    num_variables = len(rref_matrix[0])
    num_equations = len(rref_matrix)
    free_variables = [i for i in range(num_variables) if i not in pivot_indices]

    # Initialize a dictionary to store the solutions
    solutions = {var: 0 for var in range(num_variables)}

    for row_idx in range(num_equations - 1, -1, -1):
        pivot_idx = next((i for i in range(num_variables) if rref_matrix[row_idx][i] != 0), None)
        if pivot_idx is not None:
            pivot_value = rref_matrix[row_idx][pivot_idx]
            solutions[pivot_idx] = rref_matrix[row_idx][-1] / pivot_value

            # Express other variables in terms of the pivot variables
            for col_idx in range(pivot_idx + 1, num_variables - 1):
                if rref_matrix[row_idx][col_idx] != 0:
                    solutions[pivot_idx] -= (rref_matrix[row_idx][col_idx] / pivot_value) * solutions[col_idx]

    # Express free variables in terms of parameters
    for free_var in free_variables:
        solutions[free_var] = f"t{free_var}"  # Using 't' as parameter for free variables

    return solutions

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
    # matrix_A = [[0, 0, -2, 0, 7],
    #             [2, 4, -10, 6, 12],
    #             [2, 4, -5, 6, -5]]
    # vector_B = [[12],
    #             [28],
    #             [-1]]
    matrix_A = [[1, 3, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]
    vector_B = [[-3],
                [-9],
                [4]]
    # matrix_A = [[randint(1999, 9999) for _ in range(7)] for _ in range(5)]
    # vector_B = [[randint(1999, 9999) for _ in range(1)] for _ in range(5)]
    # print(f'matrix_A: {matrix_A}')
    # print(f'vector_B: {vector_B}')
    # matrix_A = [[4019, 9796, 8875, 4448, 6389, 9727, 9190], [4764, 6676, 5914, 5567, 4008, 2200, 8640], [5416, 6205, 4908, 4388, 2909, 3141, 3140], [2157, 4998, 7291, 2342, 5476, 9212, 3081], [4310, 9821, 8055, 2641, 3648, 8580, 7573]]
    # vector_B = [[8564], [6481], [6778], [9615], [8554]]
    

    # Construct the augmented matrix
    augmented_matrix = construct_augmented_matrix(matrix_A, vector_B)
    print("Augmented matrix:")
    for row in augmented_matrix:
        print(row)
    # import pdb;pdb.set_trace()

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

    pivot, non_pivot = identify_pivot_non_pivot_cols(rref_matrix)
    print(f'pivot, non_pivot: {pivot, non_pivot}')

    particular_solution = calculate_particular_solution(rref_matrix, pivot_indices=pivot)
    print(f'particular_solution: {particular_solution}')

    homogeneous_solutions = calculate_homogeneous_solutions(rref_matrix, pivot_indices=pivot)
    print(f'homogeneous_solutions: {homogeneous_solutions}')
    
    nullspace_solutions = find_nullspace_solutions(rref_matrix, pivot_indices=pivot)
    print(f'nullspace_solutions: {nullspace_solutions}')
    
    general_solutions = general_solution_from_rref(rref_matrix, pivot_indices=pivot)
    print(f'general_solutions: {general_solutions}')
    




if __name__ == '__main__':
    main()
    # main1()
    # main2()
