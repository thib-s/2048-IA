# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:57:16 2015

@author:  Valentin Levesy, Thibaut Boissin
"""

#imports###################################################################

from gamelogic import logic
from gamelogic import strategy

#CONFIGURATION#############################################################

N = 10

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
strategy.ADAPTER = False
for beta in range(10):
    strategy.BETA = beta
    resultat = []
    n = 0
    while (n < N):
        strategy.set_random_seed(n)
        board = logic.empty_board()
        score = 0
        state = 'new_tile'
        while state != 'gameover':
            if state == 'new_tile':
                logic.computer_move(strategy.choose_new_tile(None, board), board)
                state = 'direction'
            elif state == 'direction':
                direction = strategy.choose_direction(None, board, 0)
                (moved, score_increment) = logic.slide(direction, board)
                score += score_increment
                state = 'new_tile'
            if logic.game_over(board):
                state = 'gameover'
        n += 1
        resultat.append(score)
    print("****************")
    print("beta: " + str(strategy.BETA))
    print("average score = " + str(moyenne(resultat)))

            
