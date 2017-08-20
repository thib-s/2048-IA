# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 11:40:42 2016

@author: thibaut
"""

from math import log

from gamelogic import logic


def empty_tiles(board):
    """calcule le ratio de tuiles vides dans le tableau.
    cette fonction est plus rapide en execution que len(empty_tiles(board))."""
    score = 0
    for i in range(logic.SIZE):
        for j in range(logic.SIZE):
            if board[i][j] == 0:
                score += 1
    return score

def best_tile(board):
    best_tile = (0,0,0)
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            if board[x][y] > best_tile[-1]:
                best_tile = (x,y,board[x][y])
    return best_tile

def best_tile_corner(board):
    (x,y,val) = best_tile(board)
    if (((x == 0) or (x== logic.SIZE)) and ((y == 0) or (y == logic.SIZE))):
        return True
    else:
        return False

def normalize_official_score_gain(actual_score):
    return log(actual_score,2) #needs to be improved