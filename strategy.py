"""
implementation des strategies de jeu pour placer les tuiles et jouer
"""
# imports ###################################################################

import logic
import random

# configuration ############################################################

NEW_TILE_STRATEGY = 'random'

DIRECTION_STRATEGY = 'keyboard'

SCORE_FUNCTION = 'ecart'

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
    else:
        raise ValueError('No such strategy', DIRECTION_STRATEGY)

def direction_requires_keyboard():
    """indique si la strategie de direction necessite le clavier"""
    return DIRECTION_STRATEGY.startswith('keyboard')

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
