# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:57:16 2015

@author:  Valentin Levesy, Thibaut Boissin
"""

#imports###################################################################

import logic
import strategy
import score_utility
import time

#CONFIGURATION#############################################################

DIR_STRAT = ['score']
SCR_STRAT = ['ecart','basic']
TIL_STRAT = ['random']
N = 100

#FONCTIONS#################################################################

def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)

#TESTS#####################################################################

final = dict()
strategy.set_random_seed(123456789)
for dir_strat in DIR_STRAT:
    for scr_strat in SCR_STRAT:
        for til_strat in TIL_STRAT:
            strategy.DIRECTION_STRATEGY = dir_strat
            strategy.NEW_TILE_STRATEGY = til_strat
            strategy.SCORE_FUNCTION = scr_strat
            resultat = []
            n = 0
            while (n < N):
                board = logic.empty_board()
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
                resultat.append(score_utility.best_tile(board)[2])
                #print(2**(score_utility.best_tile(board)[2]))
            final[til_strat] = resultat
            print("****************")
            print("Fonction de direction: " + dir_strat)
            print("Fonction de score: " + scr_strat)
            print("Fonction choix des tuiles: " + til_strat)
            print("Nombre de parties jouées: " + str(len(resultat)))
            print("MIN = " + str(min(resultat)))
            print("MAX = " + str(max(resultat)))
            print("MOY = " + str(moyenne(resultat)))
            A = resultat.count(12)
            print("4096: " + str(A*100/N) + "%")
            A += resultat.count(11)
            print("2048: " + str(A*100/N) + "%")
            A += resultat.count(10)
            print("1024: " + str(A*100/N) + "%")
            A += resultat.count(9)
            print("512: " + str(A*100/N) + "%")
            
