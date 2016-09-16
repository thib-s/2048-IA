# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:02:59 2015
Ce fichier contient toutes fonctions qui seront utilisees par score_board
"""
import logic
import math

def mono_line(value):
    line = value[:]
    val_mono = 0
    monotony = ''
    num_of_zeros = line.count(0)
    for i in range(num_of_zeros):
        line.remove(0)
    for i in range (len(line)-1):
        new_monotony = ''
        if line[i]-line[i+1] > 0:
            new_monotony = 'desc'
            if (new_monotony != monotony) and not(monotony == ''):
                val_mono += abs(line[i]-line[i+1])
        elif line[i]-line[i+1] < 0:
            new_monotony = 'crois'
            if (new_monotony != monotony) and not(monotony == ''):
                val_mono += abs(line[i]-line[i+1])
        monotony = new_monotony
    return val_mono

def mono_board(board):
    tot_mono = 0
    for line in board:
        tot_mono += mono_line(line)
    for i in range(len(board)):
        tot_mono += mono_line(logic.get_colonne(board,i))
    return tot_mono

def best_tile(board):
    best_tile = (0,0,0)
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            if board[x][y] > best_tile[-1]:
                best_tile = (x,y,board[x][y])
    return best_tile

def best_tile_in_corner(board, bst_tile):
    s = logic.SIZE
    b = bst_tile
    if ((b[0] == 0) or (b[0] == s)) and ((b[1] == 0) or (b[1] == s)):
        return 1
    return 0

def best_tile_on_edge(board, bst_tile):
    s = logic.SIZE
    b = bst_tile
    if (b[0] == 0) or (b[0] == s) or (b[1] == 0) or (b[1] == s):
        return 1
    return 0
    
def second_best(board):
    best_tile=[(0,0,0),(0,0,0)]
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            if board[x][y] > best_tile[0][2]:
                best_tile[1]=best_tile[0]
                best_tile[0]=(x,y,board[x][y])
            elif board[x][y] > best_tile[1][2]:
                best_tile[1]=(x,y,board[x][y])
    if ((best_tile[0][1] - best_tile[1][1]) + (best_tile[0][0] - best_tile[1][0])) < 2:
        return 1
    else:
        return 0
        
def ecart(board):
    ecart=0
    for x in range(logic.SIZE-1):
        for y in range(logic.SIZE-1):
            if board[x][y] != 0:
                if board [x+1][y] != 0:
                    ecart += abs(board[x][y] - board [x+1][y])
                if board [x+1][y] != 0:
                    ecart += abs(board[x][y] - board [x][y+1])
        if ((board[x][logic.SIZE-1] != 0) and (board[x+1][logic.SIZE-1] != 0)):
            ecart += (abs(board[x][logic.SIZE-1]-board[x+1][logic.SIZE-1]))
        if (board[logic.SIZE-1][x] != 0) and (board[logic.SIZE-1][x+1] != 0):
            ecart += (abs(board[logic.SIZE-1][x] - board[logic.SIZE-1][x+1]))
    return ecart

def third_best(board):
    best_tile=[(0,0,0),(0,0,0),(0,0,0)]
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            if board[x][y] > best_tile[0][2]:
                best_tile[2]=best_tile[1]
                best_tile[1]=best_tile[0]
                best_tile[0]=(x,y,board[x][y])
            elif board[x][y] > best_tile[1][2]:
                best_tile[2]=best_tile[1]
                best_tile[1]=(x,y,board[x][y])
            elif board[x][y] > best_tile[1][2]:
                best_tile[1]=(x,y,board[x][y])
    if ((best_tile[0][1] - best_tile[1][1]) + (best_tile[0][0] - best_tile[1][0])) < 2:
        if ((best_tile[1][1] - best_tile[2][1]) + (best_tile[1][0] - best_tile[2][0])) < 2:
            return 3
        return 1
    return 0

def tile_sum(board):
    result = 0
    for line in board:
        for tile in line:
            result += 2**tile
    return math.log2(result)
    

def compress_score(values):
    """compute a left slide applied to values.
    values follow the log convention: 0 means "empty cell", and N
    means "cell containing 2 ** N".
    For example, compress([2, 2, 0, 0]) == [3, 0, 0, 0].
    """
    #OPTIMISATION A FAIRE, plutot que de copier les valeurs on peut supprimer les zeros dans value
    #du coup gain en memoire et en temps
    line = logic.zeros(logic.SIZE)
    j = 0
    for i in range(logic.SIZE):# on place tous les zeros a la fin dans line
        if values[i] != 0:
            line[j] = values[i]
            j += 1
    line.append(-1)
    score = 0
    i = 0#curseur qui lit les valeurs de line par groupe de 2
    k = 0#curseur qui indique ou on place les valeurs sur la ligne finale
    while i < j:
        if line[i] == line[i+1]:
            score += 2**(line[i]+1)
            i += 2
        else:
            i += 1
        k += 1
    return score

def slide_score(direction, board):
    """slide the board according to direction, return whether the board has changed.

    If dry_run is True, then don't change the board, just return
    whether the board would be changed.
    """
    score = 0
    if (direction == logic.LEFT) or (direction == logic.RIGHT):
        for i in range(logic.SIZE):
            score += compress_score(board[i])
    elif (direction == logic.DOWN) or (direction == logic.UP):
        for i in range(logic.SIZE):
            score += compress_score(logic.get_colonne(board, i))
    return score
