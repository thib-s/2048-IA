"""
implementation des strategies de jeu pour placer les tuiles et jouer
"""
# imports ###################################################################

import random

from gamelogic import logic
from gamelogic import scoring
from tools.Config import Config

# configuration ############################################################
DEFAULTCONFIG = {
    'tilestrat': 'random',
    'dirstrat': 'expectimax',
    'minmaxdepth': 4,
    'dynamicdepth': True,
    'alpha': 0.15,
    'beta': 1000
}

CONFIG = Config("strategy",DEFAULTCONFIG)

NEW_TILE_STRATEGY = CONFIG.getAttr('tilestrat')

DIRECTION_STRATEGY = CONFIG.getAttr('dirstrat')

GAMEOVER = -float('inf')

MINMAX_MAX_LEVEL = CONFIG.getAttr('minmaxdepth')

ADAPTED_LEVEL = MINMAX_MAX_LEVEL

ADAPTER = CONFIG.getAttr('dynamicdepth')

ALPHA = CONFIG.getAttr('alpha')

BETA = CONFIG.getAttr('beta')

#--------------------------------------#
#---------CHOIX DES STRATEGIES---------#
#--------------------------------------#

def choose_new_tile(key, board):
    """selectionne la strategie a utiliser pour placer les tuiles"""
    if NEW_TILE_STRATEGY == 'random':
        return random_tile(board)
    else:
        raise ValueError('No such strategy', NEW_TILE_STRATEGY)

def new_tile_requires_keyboard():
    """indique si la strategie de placement de tuiles necessite le clavier"""
    return NEW_TILE_STRATEGY.startswith('keyboard')

def choose_direction(key, board, score):
    """selectionne la strategie a utiliser pour choisir la direction"""
    if DIRECTION_STRATEGY == 'keyboard':
        return keyboard_choose_direction(key)
    if DIRECTION_STRATEGY == 'expectimax':
        if ADAPTER:
            adapt_level(board)
        return expectimax_direction(board,0,0,True)
    else:
        raise ValueError('No such strategy', DIRECTION_STRATEGY)

def direction_requires_keyboard():
    """indique si la strategie de direction necessite le clavier"""
    return DIRECTION_STRATEGY.startswith('keyboard')

def adapt_level(board):
    global MINMAX_MAX_LEVEL, ADAPTED_LEVEL
    score = scoring.empty_tiles(board)
    if score < 2:
        ADAPTED_LEVEL = 8
    elif score < 5:
        ADAPTED_LEVEL = 6
    elif score < 8:
        ADAPTED_LEVEL = 4
    else:
        ADAPTED_LEVEL = 4

#--------------------------------------#
#-----------CHOIX DES TUILES-----------#
#--------------------------------------#

def set_random_seed(newSeed):
    random.seed(newSeed)

# Original game's strategy to add new tile
def random_tile(board):
    """choisit l'emplacement de la tuile suivant la regle originale de 2048"""
    i, j = random.choice(logic.empty_tiles(board))
    value = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    return i, j, value

def always2_tile(board):
    """place un 2 sur une des cases encore disponibles"""
    i, j = random.choice(logic.empty_tiles(board))
    return i, j, 2

#--------------------------------------#
#---------CHOIX DES DIRECTIONS---------#
#--------------------------------------#

# Original game's strategy: keyboard
def keyboard_choose_direction(key):
    """Cette strategie utilise le clavier pour choisir la direction a prendre"""
    try:
        direction = {
            "Down":  logic.DOWN,
            "Up":    logic.UP,
            "Left":  logic.LEFT,
            "Right": logic.RIGHT,
        }[key]
    except KeyError:
        return None
    return direction

def compute_score(board, score):
    global ALPHA, BETA
    return ALPHA * scoring.empty_tiles(board) + (1 - ALPHA) * score + BETA * scoring.best_tile_corner(board)

#EXPECTIMAX###################################################################

def expectimax_direction(board, level, score = 0, first_iter=False):
    """
    Implementation de Min/Max du cote placement des tuiles + Alpha Beta
    """
    best_case = GAMEOVER
    if level == ADAPTED_LEVEL:
        return compute_score(board, score)
    for direction in logic.possible_moves(board):
        attempt = logic.copy_board(board)
        (_, score_increment) = logic.slide(direction, attempt)
        next_score = score + score_increment
        this_score = expectimax_tile(attempt, level+1, next_score)
        if (direction == logic.UP):
            this_score = 0.9*this_score
        if this_score >= best_case:
            best_case = this_score
            best_move = direction
    if first_iter:
        return best_move
    else:
        return best_case

def expectimax_tile(board, level, score = 0):
    """
    Implementation de Min/Max du cote placement des tuiles + Alpha Beta
    ici on choisit la variante expectimax qui tiens compte des probabilités de chaque situations
    """
    board = logic.copy_board(board)
    result = 0
    if level == ADAPTED_LEVEL:
        return compute_score(board, score)
    for tile in logic.empty_tiles(board):
        for tile_value in range(2, 5, 2):
            attempt = logic.copy_board(board)
            logic.computer_move((tile[0], tile[1], tile_value), attempt)
            this_score = expectimax_direction(attempt, level+1, score)
            if tile_value == 2:
                result += this_score * scoring.empty_tiles(board) * 0.9
            else:
                result += this_score * scoring.empty_tiles(board) * 0.1
    if len(logic.empty_tiles(board))==0:
        result = expectimax_direction(board, level+1, score)
    return result
