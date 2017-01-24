"""
implementation des strategies de jeu pour placer les tuiles et jouer
"""
# imports ###################################################################
import numpy as np

import logic
import random
from pybrain.structure import RecurrentNetwork, LinearLayer, SigmoidLayer, FullConnection

# configuration ############################################################

NEW_TILE_STRATEGY = 'random'

DIRECTION_STRATEGY = 'brain'

SCORE_FUNCTION = 'ecart'

BRAIN_INIT = False

NET = RecurrentNetwork()

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

def choose_direction(key, board):
    """selectionne la strategie a utiliser pour choisir la direction"""
    if DIRECTION_STRATEGY == 'keyboard':
        return keyboard_choose_direction(key)
    elif DIRECTION_STRATEGY == "brain":
        return brain_choose_direction(board)
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

def brain_choose_direction(board):
    global BRAIN_INIT
    if not BRAIN_INIT:
        brain_init()
        BRAIN_INIT = True
    return brain_decision(board)

def brain_init():
    global NET
    NET.addInputModule(LinearLayer(logic.SIZE**2, name='in'))
    NET.addModule(SigmoidLayer(logic.SIZE**2, name='hidden'))
    NET.addOutputModule(LinearLayer(4, name='out'))
    NET.addConnection(FullConnection(NET['in'], NET['hidden'], name='c1'))
    NET.addConnection(FullConnection(NET['hidden'], NET['out'], name='c2'))
    NET.addRecurrentConnection(FullConnection(NET['hidden'], NET['hidden'], name='c3'))
    NET.sortModules()
    NET.randomize()
    #set_brain_weights()

def set_brain_weights(weights):
    global NET
    NET.params = weights

def get_brain_weights():
    return NET.params

def brain_decision(board):
    global NET
    cp_board = prepare_board(board)
    result = NET.activate(cp_board)
    max_val = -float('inf')
    max_index = 0
    for i in range(len(result)):
        if result[i]>=max_val and logic.move_is_possible(logic.DIRECTIONS[i],board):
            max_index = i
            max_val = result[i]
    return logic.DIRECTIONS[max_index]

def prepare_board(board):
    return np.asarray(board).reshape(-1)


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
