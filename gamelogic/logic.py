# -*- coding: utf-8 -*-

import math

# state #####################################################################

DIRECTIONS = "up", "down", "left", "right"
UP, DOWN, LEFT, RIGHT = DIRECTIONS
SIZE = 4

# logic #####################################################################

#--------------------------------------#
#--------FONCTIONS D'AFFICHAGE---------#
#--------------------------------------#

def board_to_string(board):
    """Turn a board into a human-readable string"""
    out = ''
    for line in board:
        out += '['
        for e in line:
            out += '{:>5}'.format(2**e if e > 0 else 0)
        out += ']\n'
    return out

def value(board, i, j):
    """compute the value of board in pos(i,j) as a power of 2."""
    if board[i][j] == 0:
        return board[i][j]
    else:
        return 2 ** board[i][j]

def log2_value(board, i, j):
    """compute log_2(value(board, i, j)), or 0 if value(board, i, j) == 0."""
    return board[i][j]

#--------------------------------------#
#-----------FONCTIONS UTILES-----------#
#--------------------------------------#

def init(board):
    """init the board from a repr using powers of 2."""
    board_resul = empty_board()
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j]:
                board_resul[i][j] = round(math.log(board[i][j], 2))
    return board_resul

def empty_board():
    """renvoie un board vide"""
    res = []
    for i in range(SIZE):
        res.append(zeros(SIZE))
    return res

def zeros(N):
    """renvoie un tableau avec N zero dedans"""
    res = []
    for i in range(N):
        res.append(0)
    return res

def copy_board(board):
    """Return a copy of the board"""
    return [line[:] for line in board]


def empty_tiles(board):
    """compute the list of the coordinates of empty tiles."""
    tiles = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                tiles.append((i, j))
    return tiles

def computer_move(new_tile_move, board):
    """choose a computer move and update the board accordingly."""
    i, j, val = new_tile_move
    assert val == 2 or val == 4
    board[i][j] = val // 2

#--------------------------------------#
#--------DEPLACEMENT DES TUILES--------#
#--------------------------------------#

def compress(values):
    """compute a left slide applied to values.
    values follow the log convention: 0 means "empty cell", and N
    means "cell containing 2 ** N".
    For example, compress([2, 2, 0, 0]) == [3, 0, 0, 0].
    """
    #OPTIMISATION A FAIRE, plutot que de copier les valeurs on peut supprimer les zeros dans value
    #du coup gain en memoire et en temps
    line = zeros(SIZE)
    j = 0
    for i in range(SIZE):# on place tous les zeros a la fin dans line
        if values[i] != 0:
            line[j] = values[i]
            j += 1
    line.append(-1)
    result = zeros(SIZE)
    score_increment = 0
    i = 0#curseur qui lit les valeurs de line par groupe de 2
    k = 0#curseur qui indique ou on place les valeurs sur la ligne finale
    while i < j:
        if line[i] == line[i+1]:
            result[k] = line[i]+1
            score_increment += 2*(line[i]+1)
            i += 2
        else:
            result[k] = line[i]
            i += 1
        k += 1
    return (result,score_increment)

def slide(direction, board, dry_run=False):
    """slide the board according to direction, return whether the board has changed.

    If dry_run is True, then don't change the board, just return
    whether the board would be changed.
    """
    cp_board = copy_board(board)
    score = 0
    if direction == LEFT:
        for i in range(SIZE):
            (board[i],line_score) = compress(board[i])
            score += line_score
    elif direction == DOWN:
        for i in range(SIZE):
            (partial_slide, line_score) = compress(inverse(get_colonne(board, i)))
            set_colonne(board, inverse(partial_slide), i)
            score += line_score
    elif direction == RIGHT:
        for i in range(SIZE):
            (partial_slide, line_score) = compress(inverse(board[i]))
            board[i] = inverse(partial_slide)
            score += line_score
    elif direction == UP:
        for i in range(SIZE):
            (partial_slide, line_score) = compress(get_colonne(board, i))
            set_colonne(board, partial_slide, i)
            score += line_score
    if cp_board == board:
        return (False, score)
    else:
        if dry_run == True:
            for i in range(SIZE):#on copie le tableau ligne par ligne
                board[i] = cp_board[i]#cela evite les erreurs de pointeurs
        return (True, score)

#--------------------------------------#
#---------DIRECTIONS POSSIBLES---------#
#--------------------------------------#

def move_is_possible(direction, board):
    """verifie si le movement indiqué est possible"""
    (res, _) = slide(direction, board, True)
    return res

def possible_moves(board):
    """renvoie une liste des directions possibles"""
    moves = []
    for direction in DIRECTIONS:
        if move_is_possible(direction, board):
            moves.append(direction)
    return moves

def game_over(board):
    """check if the game is over."""
    gameover = True
    for direction in DIRECTIONS:
        if move_is_possible(direction, board):
            gameover = False
    return gameover # A FAIRE: detecter proprement les fins de jeu.

#--------------------------------------#
#---------FONCTIONS POUR SLIDE---------#
#--------------------------------------#

def inverse(values):
    """inverse l'ordre des termes de la colonne entrée"""
    result = zeros(SIZE)
    for i in range(SIZE):
        result[-(i+1)] = values[i]
    return result

def get_colonne(board, i):
    """retourne la colonne i du tableau"""
    col = zeros(SIZE)
    for j in range(SIZE):
        col[j] = board[j][i]
    return col

def set_colonne(board, col, i):
    """remplace la colonne i du board par col"""
    for j in range(SIZE):
        board[j][i] = col[j]
    return board
