# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:57:16 2015

@author:  Valentin Levesy, Thibaut Boissin
"""

#imports###################################################################

import logic
import strategy

#CONFIGURATION#############################################################

N = 50
vectors = [[1,10,600,40,35,0.5],
           [47.163933434050001, 37.059649768204814, 1005.8582246825005, 238.03858999798092, -20.466133240700227, 32.259843081820961],
[ 0.21088312,  0.58642133,  0.25750207,  0.99326141,  0.54198695,  0.50119816],
[ 0.24379714,  0.6158517 ,  0.15906075,  0.9188028,   0.50550968,  0.6032428 ]]

#FONCTIONS#################################################################

def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)
    
def scoring(board):
    result = 0
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            result = result + 2**board[x][y]
    return result

#TESTS#####################################################################

strategy.DIRECTION_STRATEGY = 'score'
strategy.NEW_TILE_STRATEGY = 'random'
strategy.SCORE_FUNCTION = 'ecart'
for v in vectors:
    resultat = []
    n = 0
    while (n < N):
        strategy.set_random_seed(n)
        board = logic.empty_board()
        strategy.V = v
        state = 'new_tile'
        while state != 'gameover':
            if state == 'new_tile':
                logic.computer_move(strategy.choose_new_tile(None, board), board)
                state = 'direction'
            elif state == 'direction':
                logic.slide(strategy.choose_direction(None, board), board)
                state = 'new_tile'
            if logic.game_over(board):
                state = 'gameover'
        n += 1
        resultat.append(scoring(board))
    print("****************")
    print("Vecteur: " + str(v))
    print("score = " + str(moyenne(resultat)))
            
