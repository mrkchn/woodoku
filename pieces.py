import numpy as np
import itertools

SHAPE = (9, 9)
BOARD = np.zeros(SHAPE, dtype=int)
NUM_REGIONS = 3
NUM_PIECES = 3
LINES = [np.ones((1, length), dtype=int) for length in range(2, 6)]
LS = [np.array([[1, 0],
                [1, 1]]),
      np.array([[1, 0, 0],
                [1, 0, 0],
                [1, 1, 1]]),
      np.array([[1, 0],
                [1, 0],
                [1, 1]]),
      np.array([[0, 1],
                [0, 1],
                [1, 1]])]
CROSSES = [np.array([[0, 1, 0],
                     [1, 1, 1],
                     [0, 1, 0]])]
ZS = [np.array([[1, 0],
                [1, 1],
                [0, 1]])]
SQUARES = [np.array([[1, 1],
                     [1, 1]])]
UNITS = [np.array([[1]])]
DIAGONALS = [np.identity(n, dtype=int) for n in range(2, 5)]
TS = [np.array([[0, 1, 0],
                [1, 1, 1]]),
      np.array([[0, 1, 0],
                [0, 1, 0],
                [1, 1, 1]])]

PIECES = LINES + LS + CROSSES + ZS + SQUARES + UNITS + DIAGONALS + TS
PIECES = list(itertools.chain.from_iterable([[np.rot90(piece, k) for k in range(4)] for piece in PIECES]))