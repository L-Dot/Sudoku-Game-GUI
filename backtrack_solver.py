import numpy as np

testgrid = np.array([[0,1,0,0,3,0,9,0,2],
                    [0,0,0,0,0,2,0,1,0],
                    [0,6,2,7,0,8,5,0,0],
                    [1,7,0,8,4,3,6,2,9],
                    [0,4,3,6,0,0,1,7,0],
                    [0,2,9,0,0,5,8,0,3],
                    [3,8,0,0,0,1,0,9,0],
                    [0,0,0,2,0,0,3,8,7],
                    [2,9,0,3,8,0,4,5,0]])


## Backtracking algorithm ##
# Filling in a number and testing if it is valid. If not then go back and try the next number.

def row_check(grid, M):
    """Given a M x N grid and rownumber M, returns True/False depending
     on if there are multiple of the same number in the row."""

    row = grid[M]
    row = row[row != 0]

    for num in row:
        count = (row == num).sum()
        if count >= 2:
            return False
    return True

def col_check(grid, N):
    """Given a M x N grid and columnnumber N, returns True/False depending
     on if there are multiple of the same number in the column."""

    col = grid.T[N]
    col = col[col != 0]

    for num in col:
        count = (col == num).sum()
        if count >= 2:
            return False
    return True


def box_check(grid, M, N):
    """Given a M x N grid, rownumber M and columnnumber N, returns True/False depending
     on if there are multiple of the same number in the corresponding 3x3 box."""

    if M < 3:
        M = 0
    elif 3 <= M < 6:
        M = 3
    elif M >= 6:
        M = 6

    if N < 3:
        N = 0
    elif 3 <= N < 6:
        N = 1
    elif N >= 6:
        N = 2

    block = grid.reshape(27,3)[N + 3*M : N + 9 + 3*M : 3].flatten()
    block = block[block != 0]

    for num in block:
        count = (block == num).sum()
        if count >= 2:
            return False
    return True

def backtrack(grid):
    """Solves any given 9x9 grid of solvable sudoku."""

    M = 0
    N = 0
    solved_grid = grid.copy().flatten()
    empty_spaces = np.where(solved_grid.flatten() == 0)[0]

    i = 0
    while i != len(empty_spaces):

        empty_space = empty_spaces[i]
        M = empty_space // 9
        N = empty_space % 9

        solved_grid[empty_space] = solved_grid[empty_space] + 1

        if row_check(solved_grid.reshape(9,9), M) and col_check(solved_grid.reshape(9,9), N) \
            and box_check(solved_grid.reshape(9,9), M, N) and solved_grid[empty_space] != 10:
            i = i + 1
            continue
        else:
            if solved_grid[empty_space] >= 9 and i != 0:
                solved_grid[empty_space] = 0
                i = i - 1
                continue
            else:
                continue

    return solved_grid.reshape(9,9)

print(backtrack(testgrid))