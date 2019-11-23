#!/usr/bin/env python3

# Author: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2010 Ali Assaf
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product
import time
def solve_sudoku(size, grid):
    """ An efficient Sudoku solver using Algorithm X.

    >>> grid = [
    ...   [8, 7, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 13, 0, 4, 0],
    ...   [0, 5, 14, 0, 0, 0, 3, 10, 15, 9, 1, 0, 0, 6, 0, 0],
    ...   [16, 0, 0, 0, 5, 8, 7, 0, 0, 14, 0, 0, 9, 0, 11, 12],
    ...   [0, 0, 4, 0, 0, 14, 6, 13, 0, 11, 10, 12, 0, 7, 0, 3],
    ...   [14, 0, 0, 8, 0, 0, 1, 0, 0, 0, 0, 3, 7, 4, 12, 0],
    ...   [9, 0, 0, 0, 0, 6, 15, 12, 0, 0, 13, 14, 0, 3, 1, 0],
    ...   [11, 0, 10, 3, 0, 0, 13, 0, 0, 8, 0, 1, 0, 0, 6, 0],
    ...   [6, 0, 0, 1, 14, 0, 4, 0, 0, 5, 0, 9, 11, 0, 0, 13],
    ...   [0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 9, 0, 5, 0, 2, 10],
    ...   [10, 1, 0, 0, 6, 0, 5, 0, 13, 15, 7, 16, 0, 0, 0, 0],
    ...   [0, 0, 16, 11, 0, 4, 0, 8, 2, 0, 0, 0, 0, 13, 0, 7],
    ...   [0, 9, 0, 7, 1, 3, 0, 2, 6, 0, 8, 10, 16, 15, 14, 4],
    ...   [7, 0, 13, 0, 9, 16, 0, 5, 0, 0, 14, 4, 3, 8, 0, 2],
    ...   [0, 0, 3, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 16, 15, 0],
    ...   [1, 0, 9, 0, 0, 0, 14, 4, 0, 0, 0, 0, 0, 0, 7, 0],
    ...   [0, 6, 8, 0, 3, 0, 0, 0, 10, 7, 0, 0, 0, 0, 0, 0]]
    >>> for solution in solve_sudoku((4, 4), grid):
    ...     print(*solution, sep='\\n')
        [8, 7, 11, 10, 2, 12, 9, 1, 5, 3, 16, 6, 13, 14, 4, 15]
        [12, 5, 14, 13, 4, 11, 3, 10, 15, 9, 1, 7, 2, 6, 16, 8]
        [16, 3, 1, 6, 5, 8, 7, 15, 4, 14, 2, 13, 9, 10, 11, 12]
        [2, 15, 4, 9, 16, 14, 6, 13, 8, 11, 10, 12, 1, 7, 5, 3]
        [14, 13, 15, 8, 11, 2, 1, 9, 16, 10, 6, 3, 7, 4, 12, 5]
        [9, 4, 7, 5, 8, 6, 15, 12, 11, 2, 13, 14, 10, 3, 1, 16]
        [11, 2, 10, 3, 7, 5, 13, 16, 12, 8, 4, 1, 15, 9, 6, 14]
        [6, 16, 12, 1, 14, 10, 4, 3, 7, 5, 15, 9, 11, 2, 8, 13]
        [3, 8, 6, 12, 15, 13, 16, 7, 14, 4, 9, 11, 5, 1, 2, 10]
        [10, 1, 2, 4, 6, 9, 5, 14, 13, 15, 7, 16, 8, 12, 3, 11]
        [15, 14, 16, 11, 12, 4, 10, 8, 2, 1, 3, 5, 6, 13, 9, 7]
        [13, 9, 5, 7, 1, 3, 11, 2, 6, 12, 8, 10, 16, 15, 14, 4]
        [7, 11, 13, 15, 9, 16, 12, 5, 1, 6, 14, 4, 3, 8, 10, 2]
        [5, 12, 3, 14, 10, 7, 8, 6, 9, 13, 11, 2, 4, 16, 15, 1]
        [1, 10, 9, 2, 13, 15, 14, 4, 3, 16, 5, 8, 12, 11, 7, 6]
        [4, 6, 8, 16, 3, 1, 2, 11, 10, 7, 12, 15, 14, 5, 13, 9]
    """
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

if __name__ == "__main__":
    import doctest
    start = time.process_time()
    doctest.testmod()
    end = time.process_time()
    print(end - start)
