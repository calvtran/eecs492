import numpy as np
import sys
import copy
import queue

'''
File reading function for sudoku
Input: filename
Output: a list of 2D numpy matrices representing sudokus. Each of these sudoku boards is a 9x9 numpy matrix of integers.
board[r, c] will access the number set in the Sudoku board at the row r and the column c. A value from 1-9 means that
value is set and must have that value. A value of 0 means that position is blank.
'''
def read_sudoku(fname):
    with open(fname) as f:
        f_input = [x.strip('\r\n') for x in f.readlines()]

    sudoku_list = []
    for i in range(len(f_input)):
        sudoku = np.zeros((9, 9), dtype=np.int64)
        temp = f_input[i]
        for j in range(0, len(temp), 9):
            sudoku_row = temp[j:j + 9]
            for k in range(0, 9):
                sudoku[int(j / 9)][k] = sudoku_row[k]
        sudoku_list.append(sudoku)

    return sudoku_list

'''Write all of the puzzles to a file.'''
def write_all_sudokus(filename, sudoku_list):
    with open(sys.argv[2], 'w') as write_file:
        for s in sudoku_list:
            write_sudoku(write_file, s)

'''Write a single sudoku solution to a file'''
def write_sudoku(f, sudoku):
    for i in sudoku.flatten():
        f.write(str(i))
    f.write('\n')

'''
Printing function for sudoku,
Input: a 2D numpy matrix
'''
def print_sudoku(sudoku):
    print('+-------+-------+-------+')
    for i in range(0, 9):
        c = [str(i) if i != 0 else '*' for i in sudoku[i]]
        print("| {} {} {} | {} {} {} | {} {} {} |".format(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8]))
        if (i + 1) % 3 == 0:
            print('+-------+-------+-------+')

'''
Utility function for getting coordinates of all spaces that are affected by this one
Input: coordinate: (row, col) or [row, col]
Output: a list of all other coordinates that are either in this coordinate's block
in its row, or in its column
'''
def get_neighbors(coordinate):
    neighbors = set()
    row_start = 3 * (coordinate[0] // 3)
    col_start = 3 * (coordinate[1] // 3)
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            neighbors.add((i, j))
    for i in range(9):
        neighbors.add((coordinate[0], i))
    for i in range(9):
        neighbors.add((i, coordinate[1]))
    neighbors.remove((coordinate[0], coordinate[1]))
    return list(sorted(neighbors))

'''
AC-3 Algorithm
Input: 9x9 array of sets containing the domain for each space
Output: if the AC-3 reduces a domain to have size 0 (meaning the puzzle cannot be solved), return (False, None).
Otherwise, return (True, new_domains) where new_domains is a 9x9 array of sets containing domains, the result of
performing AC-3 on the problem. 

You don't actually need to copy domains, you can just modify the input and
return (True, domains) if you want.
'''
def ac3(domains):
    #TODO Implement this!
    q = set()
    for r in range(len(domains)):
        for c in range(len(domains[r])):
            X_i = (r, c)
            arcs = get_neighbors(X_i)
            for i in range(len(arcs)):
                X_j = arcs[i]
                q.add( (X_i, X_j) )

    while len(q) > 0:
        x = q.pop()
        X_i = x[0]
        X_j = x[1]
        if revise(domains, X_i, X_j):
            if len(domains[X_i[0]][X_i[1]]) == 0:
                return False, None
            neighbors = get_neighbors(X_i)
            for k in range(len(neighbors)):
                if neighbors[k] != X_j:
                    q.add( (neighbors[k], X_i) )

    return True, domains


def revise(domains, X_i, X_j):
    revised = False
    remove = []
    for x in domains[X_i[0]][X_i[1]]:
        satisfied = False
        for y in domains[X_j[0]][X_j[1]]:
            if x != y:
                satisfied = True
                break
        if not satisfied:
            remove.append(x)
            revised = True

    for r in range(len(remove)):        
        domains[X_i[0]][X_i[1]].discard(remove[r])
    return revised
                
def get_arcs(domains):
    arcs = set()
    for r in range(len(domains)):
        for c in range(len(domains[r])):
            X_i = (r, c)
            arcs_i = get_neighbors(X_i)
            for i in range(len(arcs_i)):
                X_j = arcs_i[i]
                arcs.add( (X_i, X_j) )
    return arcs



'''
Checks whether the assignment is complete, which is when all domains have only 1 value remaining
'''
def is_assignment_complete(domains):
    return all((all((len(space) == 1 for space in domain_row)) for domain_row in domains))

'''
Utility function for seeing if the sudoku puzzle is solved.
Input: 9x9 numpy matrix
Output: bool- True if solved, False otherwise
'''
def is_solved(sudoku):
    for i in range(9):
        for num in range(1, 10):
            block_coord = [(i * 9) // 9, (i * 9) % 9]

            row_range = [3 * (block_coord[1] // 3), 3 * (block_coord[1] // 3) + 3]
            col_range = [3 * (block_coord[0] // 3), 3 * (block_coord[0] // 3) + 3]
            block = sudoku[col_range[0]:col_range[1], row_range[0]:row_range[1]]

            if (not num in sudoku[:, i]) or (not num in sudoku[i, :]) or \
                    (not num in block):
                return False
    return True

'''
Computes the initial domains for the sudoku puzzle: 1-9 unless the space is filled in
'''
def get_domains(sudoku):
    return [[{1, 2, 3, 4, 5, 6, 7, 8, 9} if sudoku[i, j] == 0 else {sudoku[i, j]}
             for j in range(9)] for i in range(9)]

'''
Backtracking search Algorithm
Inputs: domains: 9x9 array. Each element in the array is a set which should contain the current domain of the 
space. For example, if domains[1][3] = {1,2,7} is means that the 2nd row, 4th column can take values 1, 2 and 7.
Output: return True if a solution is found, with all 9x9 elements of the solution reduced to just 1 element and 
the backtracking count. If no solution is found, return False otherwise, with None and the backtracking count.
'''
def bts(domains):
    # Start by using AC-3 to reduce the initial domains
    still_valid, domains = ac3(domains)
    # If for some reason AC-3 fails here, this was apparently an impossible Sudoku
    if still_valid:
        return backtrack(domains, bt_count=0)
    else:
        return False, None, 0

"""
Helper function for BTS. bt_count just keep tracks of how many times that we have backtracked.
"""
def backtrack(domains, bt_count=0):
    if is_assignment_complete(domains):
        return True, domains, bt_count

    # Find the minimum remaining value
    min_i = 0
    min_j = 0
    for i in range(9):
        for j in range(9):
            # We will assign the smallest domain with more than 1 element
            if len(domains[min_i][min_j]) <= 1 or \
                    (len(domains[i][j]) > 1 and len(domains[i][j]) < len(domains[min_i][min_j])):
                min_i = i
                min_j = j
    assert len(domains[min_i][min_j]) > 1

    # This is the location of the minimum remaining value
    coord = (min_i, min_j)

    # The book discusses potentially reordering this list to choose more promising values first.
    # Don't worry about that.
    for possible_value in domains[coord[0]][coord[1]]:
        # Check for consistency with neighbors if we assign this value
        if all((coord == n or any((possible_value != val for val in domains[n[0]][n[1]])) \
                for n in get_neighbors(coord))):
            domains_with_assignment = copy.deepcopy(domains)
            domains_with_assignment[coord[0]][coord[1]] = {possible_value}
            # Inference step
            still_valid, domains_with_assignment = ac3(domains_with_assignment)
            # If this fails, this assignment doesn't work. Skip to backtracking.
            if still_valid:
                solved, solution, bt_count = backtrack(domains_with_assignment, bt_count)
                if solved:
                    return True, solution, bt_count
            bt_count += 1

    return False, None, bt_count

'''
Main function
'''
def main():
    sudoku_list = read_sudoku(sys.argv[1])

    solved_sudokus = []
    for sudoku in sudoku_list:
        print_sudoku(sudoku)
        print('Using backtracking search')
        domains = get_domains(sudoku)
        solved, domains, count = bts(domains)
        if solved:
            print('Solved Sudoku')
            for i in range(9):
                for j in range(9):
                    sudoku[i, j] = domains[i][j].pop()
            print_sudoku(sudoku)
            assert is_solved(sudoku)
        else:
            print('No solution found')
        print('Backtracking count: %s' % count)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 input-filename')
    else:
        main()
