"""
implementation des strategies de jeu pour placer les tuiles et jouer
"""
# imports ###################################################################

from multiprocessing import Pool
import logic
import random
import score_utility

# configuration ############################################################

NEW_TILE_STRATEGY = 'random'

ALPHA_BETA = True

MEMO = False

MEMO_DIC = dict()

EXPECTIMAX = True

DIRECTION_STRATEGY = 'minmax'

MINMAX_MAX_LEVEL = 4

GAMEOVER = -10000000

SCORE_COEF = 1

SCORE_FUNCTION = 'ecart'

V =  [47.16393343405, 37.059649768204814, 1005.8582246825005, 238.03858999798092, -20.466133240700227, 32.25984308182096]


#--------------------------------------#
#---------CHOIX DES STRATEGIES---------#
#--------------------------------------#

def choose_new_tile(key, board):
    """selectionne la strategie a utiliser pour placer les tuiles"""
    if NEW_TILE_STRATEGY == 'random':
        return random_tile(board)
    elif NEW_TILE_STRATEGY == 'always2':
        return always2_tile(board)
    elif NEW_TILE_STRATEGY == 'minmax_worst':
        return minmax_worst_tile(board)
    elif NEW_TILE_STRATEGY == 'minmax_best':
        return minmax_best_tile(board)
    else:
        raise ValueError('No such strategy', NEW_TILE_STRATEGY)

def new_tile_requires_keyboard():
    """indique si la strategie de placement de tuiles necessite le clavier"""
    return NEW_TILE_STRATEGY.startswith('keyboard')

def choose_direction(key, board):
    """selectionne la strategie a utiliser pour choisir la direction"""
    if DIRECTION_STRATEGY == 'keyboard':
        return keyboard_choose_direction(key)
    elif DIRECTION_STRATEGY == 'random':
        return random_choose_direction()
    elif DIRECTION_STRATEGY == 'priority':
        return priority_choose_direction(board)
    elif DIRECTION_STRATEGY == 'score':
        return score_choose_direction(board)
    elif DIRECTION_STRATEGY == 'minmax':
        return minmax_choose_direction(board)
    else:
        raise ValueError('No such strategy', DIRECTION_STRATEGY)

def score_board(board):
    """selectionne la fonction de score"""
    if SCORE_FUNCTION == 'basic':
        return SCORE_COEF*score_basic(board)
    elif SCORE_FUNCTION == 'monotony':
        return SCORE_COEF*score_mono(board)
    elif SCORE_FUNCTION == 'corner_edge':
        return SCORE_COEF*score_corner(board)
    elif SCORE_FUNCTION == 'second_best':
        return SCORE_COEF*score_second_best(board)
    elif SCORE_FUNCTION == 'third_best':
        return SCORE_COEF*score_third_best(board)
    elif SCORE_FUNCTION == 'ecart':
        return SCORE_COEF*third_ecart(board)
    else:
        raise ValueError('No such score function', SCORE_FUNCTION)

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

def random_choose_direction():
    """Cette strategie prends les directions au hasard"""
    return logic.DIRECTIONS[random.randint(0, 3)]

def priority_choose_direction(board):#FAIRE LES TESTS
    """cette IA joue les coups autant que possible dans la meme direction.
    Ces directions sont placees par ordre de priorite dans le tableau prioity direction"""
    priority_directions = [logic.RIGHT,
                           logic.DOWN,
                           logic.LEFT,
                           logic.UP]
    dir_found = False
    i = 0
    while not dir_found:
        if logic.move_is_possible(priority_directions[i], board):
            dir_found = True
        else:
            i += 1
    return priority_directions[i]


def score_choose_direction(board):
    """Pick the direction that result the maximal score"""
    best_move = None
    best_score = None
    for move in logic.possible_moves(board):
        cp_board = logic.copy_board(board)
        logic.slide(move, cp_board)
        this_score = score_board(cp_board)
        if (best_move is None) or (this_score > best_score):
            best_score = this_score
            best_move = move
    return best_move
    

def minmax_choose_direction(board):
    """Pick the direction that result the maximal score using minmax"""
    global MINMAX_MAX_LEVEL
    score = score_basic(board)
    if score < 2:
        MINMAX_MAX_LEVEL = 8
    elif score < 5:
        MINMAX_MAX_LEVEL = 6
    elif score < 8:
        MINMAX_MAX_LEVEL = 4
    else:
        MINMAX_MAX_LEVEL = 4
    return call_minmax_direction(board)

#--------------------------------------#
#----------FONCTIONS DE SCORE----------#
#--------------------------------------#

def score_basic(board):
    """compte le nombre de tuiles vides dans le tableau.
    cette fonction est plus rapide en execution que len(empty_tiles(board))."""
    score = 0
    for i in range(logic.SIZE):
        for j in range(logic.SIZE):
            if board[i][j] == 0:
                score += 1
    return score

def score_mono(board):
    """cette fonction tient compte aussi de la monotonicite du tableau"""
    empty_tiles = score_basic(board)
    non_monotonicity = score_utility.mono_board(board)
    return 10 * empty_tiles - 2 * non_monotonicity

def score_corner(board):
    """cette fonction tient compte de
    -les memes choses que mono
    -la meilleure tuile
    -la position de cette meilleure tuile"""
    sc_mono = score_mono(board)
    bst_tile = score_utility.best_tile(board)
    best_tile_in_corner = score_utility.best_tile_in_corner(board, bst_tile)
    best_tile_on_edge = score_utility.best_tile_on_edge(board, bst_tile)
    if score_basic(board) == 0:
        return -20000000
    if score_basic(board) == (logic.SIZE**2 - 1):
        return 100000000
    return V[0]*sc_mono + V[1]*bst_tile[2] + V[2] * best_tile_in_corner + V[3] * best_tile_on_edge
    
def score_second_best(board):
    """cette fonction tient compte de:
    -les mêmes choses que score_corner
    -si la seconde meilleure tuile est collée à la première"""
    sc_corner = score_corner(board)
    sc_second = score_utility.second_best(board)
    return sc_corner + 40*sc_second

def score_third_best(board):
    """cette fonction tient compte de:
    -les mêmes choses que score_corner
    -si la seconde meilleure tuile est collée à la première & troisieme collée a la seconde"""
    sc_corner = score_corner(board)
    sc_third = score_utility.third_best(board)
    return sc_corner + 35*sc_third
    
def third_ecart(board):
    sc_mono = score_mono(board)
    bst_tile = score_utility.best_tile(board)
    best_tile_in_corner = score_utility.best_tile_in_corner(board, bst_tile)
    best_tile_on_edge = score_utility.best_tile_on_edge(board, bst_tile)
    if score_basic(board) == 0:
        return -20000000
    if score_basic(board) == (logic.SIZE**2 - 1):
        return 100000000
    sc_third = score_utility.third_best(board)
    ecart = score_utility.ecart(board)
    return V[0]*sc_mono + V[1]*bst_tile[2] + V[2] * best_tile_in_corner + V[3] * best_tile_on_edge + V[4]*sc_third - V[5] * ecart

#def third_ecart(board):
#    """Cette fonction tient compte de:
#    -les memes choses que third_best
#    -l'ecart en valeur absolue entre une case non nulle et ses voisines"""  
#    third = score_third_best(board)
#    ecart = score_utility.ecart(board)
#    return (third - 0.5 * ecart) *0.1


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

def minmax_worst_tile(board):
    """place la pire tuile pour le joueur, suivant l'algorithme minmax"""
    return call_minmax_tile(board)

def minmax_best_tile(board):
    """place la meilleure tuile pour le joueur, suivant l'algorithme minmax"""
    global SCORE_COEF
    SCORE_COEF = -1
    result = call_minmax_tile(board)
    SCORE_COEF = 1
    return result

#--------------------------------------#
#-----IMPLEMENTATION DE MIN/MAX--------#
#--------------------------------------#
def call_minmax_direction(board):
    """choisit la fonction a appeler selon que l'on veuille l'elagage alpha-beta, la memoisation, ou non"""
    if EXPECTIMAX:
        return expectimax_direction_multi(board, 0)
    elif MEMO:
        return minmax_direction_memo(board, 0, -float('inf'), float('inf'), True)
    elif ALPHA_BETA:
        return minmax_direction_alpha(board, 0, -float('inf'), float('inf'), True)
    else:
        return minmax_direction(board, 0, True)

def call_minmax_tile(board):
    """choisit la fonction a appeler selon que l'on veuille l'elagage alpha-beta ou non"""
    if ALPHA_BETA:
        return minmax_tile_alpha(board, 0, -float('inf'), float('inf'), True)
    else:
        return minmax_tile(board, 0, True)

def minmax_direction(board, level, first_iter=False):
    """
    Implementation de Min/Max du cote placement des tuiles
    """
    best_case = GAMEOVER
    if level == MINMAX_MAX_LEVEL:
        return score_board(board)
    for direction in logic.possible_moves(board):
        attempt = logic.copy_board(board)
        logic.slide(direction, attempt)
        this_score = minmax_tile(attempt, level+1)
        if this_score >= best_case:
            best_case = this_score
            best_move = direction
    if first_iter:
        return best_move
    else:
        return best_case

def minmax_tile(board, level, first_iter=False):
    """
    Implementation de Min/Max du cote placement des tuiles
    """
    best_case = 100000000
    board = logic.copy_board(board)
    if level == MINMAX_MAX_LEVEL:
        return score_board(board)
    for tile in logic.empty_tiles(board):
        for tile_value in range(2, 5, 2):
            attempt = logic.copy_board(board)
            logic.computer_move((tile[0], tile[1], tile_value), attempt)
            this_score = minmax_direction(attempt, level+1)
            if this_score <= best_case:
                best_case = this_score
                best_tile = (tile[0], tile[1], tile_value)
    if best_case == 10000000:
        best_case = GAMEOVER
    if first_iter:
        return best_tile
    return best_case

#elagage alpha-beta:

def minmax_direction_alpha(board, level, alpha, beta, first_iter=False):
    """
    Implementation de Min/Max du cote placement des tuiles
    on fait aussi l'élagage alpha-beta
    """
    best_case = GAMEOVER
    if level == MINMAX_MAX_LEVEL:
        return score_board(board)
    for direction in logic.possible_moves(board):
        attempt = logic.copy_board(board)
        logic.slide(direction, attempt)
        this_score = minmax_tile_alpha(attempt, level+1, alpha, beta)
        if this_score >= best_case:
            best_case = this_score
            best_move = direction
        if this_score > beta:
            if first_iter == False:
                return best_case
            else:
                return best_move
        if best_case >= alpha:
            alpha = this_score
    if first_iter:
        return best_move
    else:
        return best_case

def minmax_tile_alpha(board, level, alpha, beta, first_iter=False):
    """
    Implementation de Min/Max du cote placement des tuiles
    on fait aussi l'élagage alpha-beta
    """
    best_case = 10000000
    board = logic.copy_board(board)
    if level == MINMAX_MAX_LEVEL:
        return score_board(board)
    for tile in logic.empty_tiles(board):
        for tile_value in range(2, 5, 2):
            attempt = logic.copy_board(board)
            logic.computer_move((tile[0], tile[1], tile_value), attempt)
            this_score = minmax_direction_alpha(attempt, level+1, alpha, beta)
            if this_score <= best_case:
                best_case = this_score
                best_tile = (tile[0], tile[1], tile_value)
            if this_score < alpha:
                if first_iter == False:
                    return best_case
                else:
                    return best_tile
            if best_case <= beta:
                beta = this_score
    if best_case == 1000000:
        best_case = GAMEOVER
    if first_iter:
        return best_tile
    return best_case


#memoisation##################################################################
def minmax_direction_memo(board, level, alpha, beta, first_iter=False):
    """
    Implementation de Min/Max du cote placement des tuiles
    on fait aussi l'élagage alpha-beta
    on utilise également la mémoisation
    """
    best_case = GAMEOVER
    if level == MINMAX_MAX_LEVEL:
        return score_board(board)
    for direction in logic.possible_moves(board):
        attempt = logic.copy_board(board)
        logic.slide(direction, attempt)
        #memoisation
        try:
            this_score = MEMO_DIC[logic.board_to_string(attempt), alpha, beta, level+1, MINMAX_MAX_LEVEL]
        except:
            this_score = minmax_tile_memo(attempt, level+1, alpha, beta)
            MEMO_DIC[logic.board_to_string(attempt), alpha, beta, level+1, MINMAX_MAX_LEVEL] = this_score
        if this_score >= best_case:
            best_case = this_score
            best_move = direction
        if this_score > beta:
            if first_iter == False:
                return best_case
            else:
                return best_move
        if best_case >= alpha:
            alpha = this_score
    if first_iter:
        return best_move
    else:
        return best_case

def minmax_tile_memo(board, level, alpha, beta, first_iter=False):
    """
    Implementation de Min/Max du cote placement des tuiles
    on fait aussi l'élagage alpha-beta
    on utilise egalement la memoisation
    """
    best_case = 100000000
    board = logic.copy_board(board)
    if level == MINMAX_MAX_LEVEL:
        return score_board(board)
    for tile in logic.empty_tiles(board):
        for tile_value in range(2, 5, 2):
            attempt = logic.copy_board(board)
            logic.computer_move((tile[0], tile[1], tile_value), attempt)
            #memoisation
            try:
                this_score = MEMO_DIC[logic.board_to_string(attempt), alpha, beta, level+1, MINMAX_MAX_LEVEL]
            except:
                this_score = minmax_direction_memo(attempt, level+1, alpha, beta)
                MEMO_DIC[logic.board_to_string(attempt), alpha, beta, level+1, MINMAX_MAX_LEVEL] = this_score
            if this_score <= best_case:
                best_case = this_score
                best_tile = (tile[0], tile[1], tile_value)
            if this_score < alpha:
                if first_iter == False:
                    return best_case
                else:
                    return best_tile
            if best_case <= beta:
                beta = this_score
    if best_case == 100000000:
        best_case = GAMEOVER
    if first_iter:
        return best_tile
    return best_case

#EXPECTIMAX###################################################################

def expectimax_direction(board, level, first_iter=False):
    """
    Implementation de Min/Max du cote placement des tuiles + Alpha Beta
    """
    best_case = GAMEOVER
    if level == MINMAX_MAX_LEVEL:
        return 0.2*score_board(board)
    for direction in logic.possible_moves(board):
        attempt = logic.copy_board(board)
        current_score = score_utility.slide_score(direction, attempt )
        logic.slide(direction, attempt)
        this_score = current_score + expectimax_tile(attempt, level+1)
        if this_score >= best_case:
            best_case = this_score
            best_move = direction
    if first_iter:
        return best_move
    else:
        return best_case

def expectimax_tile(board, level):
    """
    Implementation de Min/Max du cote placement des tuiles + Alpha Beta
    ici on choisit la variante expectimax qui tiens compte des probabilités de chaque situations
    """
    board = logic.copy_board(board)
    result = 100000000
    if level == MINMAX_MAX_LEVEL:
        return score_board(board)
    for tile in logic.empty_tiles(board):
        for tile_value in range(2, 5, 2):
            attempt = logic.copy_board(board)
            logic.computer_move((tile[0], tile[1], tile_value), attempt)
            this_score = expectimax_direction(attempt, level+1)
            if tile_value == 2:
                result += (this_score / score_basic(board))*0.9
            else:
                result += (this_score / score_basic(board))*0.1
    return result
    
#EXPECTIMAX MULTITHREAD###########################################################

def expectimax_direction_multi(board, level):
    """
    Implementation de Min/Max du cote placement des tuiles + Alpha Beta
    """
    best_case = GAMEOVER
    if level == MINMAX_MAX_LEVEL:
        return score_board(board)
    pool = Pool(processes=8)
    pw = PoolWorker(board, level)
    for (this_score,direction) in pool.imap_unordered(pw.f, logic.possible_moves(board)):
        if direction == logic.DOWN:
            this_score = this_score * 0.8
        if this_score >= best_case:
            best_case = this_score
            best_move = direction
    pool.terminate()
    pool.join()
    return best_move

class PoolWorker:    
    def __init__(self, board, level):
        self.b = board
        self.l = level
    
    def f(self, direction):
        attempt = logic.copy_board(self.b)
        current_score = score_utility.slide_score(direction, attempt )
        logic.slide(direction, attempt)
        return (current_score + expectimax_tile(attempt, self.l+1), direction)

