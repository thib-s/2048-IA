# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 11:40:42 2016

@author: thibaut
"""

import logic
from math import log

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

def normalize_official_score_gain(actual_score):
    return log(actual_score,2) #needs to be improved
