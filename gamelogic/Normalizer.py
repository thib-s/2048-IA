import math

from gamelogic import scoring
from gamelogic import logic


def normalize(board):
    """
    normalize the board to limit the size of the dataset
    """
    return round_normalize(scale_normalize(board))


def scale_normalize(board):
    """
    perform a scale normalization of a board
    every tile will be replaced by it ratio to the max value on the board
    this way the two following board will have the same output:

    0 0 0 0         0 0 0 0
    0 0 0 0         0 0 0 0
    0 0 0 0         0 0 0 0
    4 4 2 0         8 8 4 0
    """
    new_board = logic.copy_board(board)
    (x, y, bestVal) = scoring.best_tile(new_board)
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            new_board[x][y] = new_board[x][y] / bestVal
    return new_board


def round_normalize(board):
    """
    as the results board of the previous function are fractions
    we round the numbers
    """
    new_board = logic.copy_board(board)
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            new_board[x][y] = math.trunc(new_board[x][y] * 10) / 10
    return new_board
