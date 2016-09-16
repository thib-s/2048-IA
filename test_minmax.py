# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:32:23 2015
Module de test des Fonctions du fichier strategy.py
@author: Valentin Levesy, Thibaut Boissin
"""
#imports###################################################################

import random
import strategy
import logic
import time

#CONFIGURATION#############################################################

TESTS = 25

#FONCTIONS#################################################################

def start_test(name):
    print("*********** start test: " + name + " *******************")

def random_board():
    board = logic.empty_board()
    for i in range(logic.SIZE):
        for j in range(logic.SIZE):
            board[i][j] = random.randint(0, 5)
    return board

#TESTS#####################################################################

start_test('verification de l\'elagage alpha beta')
tps_minmax = 0
tps_alpha = 0

for i in range(TESTS):
    board = random_board()
    
    debut = time.clock()
    alphabeta = strategy.minmax_direction_alpha(board, 0, -float('inf'), float('inf'), True)
    fin = time.clock()
    
    tps_alpha += (fin - debut)
    
    debut = time.clock()
    minmax = strategy.minmax_direction(board, 0, True)
    fin = time.clock()
    
    tps_minmax += (fin - debut)
    
    assert alphabeta == minmax
print("temps moyen minmax =" + str(tps_minmax/TESTS) + " ")
print("temps moyen alpha =" + str(tps_alpha/TESTS) + " ")

print()
print("    minmax alpha beta and minmax have the same results")
print()

start_test('verification de la memoisation')

for i in range(TESTS):
    board = random_board()
    alphabeta = strategy.minmax_direction_alpha(board, 0, -float('inf'), float('inf'), True)
    memo = strategy.minmax_direction_memo(board, 0, -float('inf'), float('inf'), True)
    assert memo == alphabeta

print("les fonctions donnent les memes résultats")

tps_alpha = 0
tps_memo = 0
board = random_board()
for i in range(TESTS):
    
    debut = time.clock()
    direction = strategy.minmax_direction_alpha(board, 0, -float('inf'), float('inf'), True)
    fin = time.clock()    
    
    tps_alpha += (fin - debut)
    
    strategy.MEMO_DIC = dict()
    debut = time.clock()
    direction = strategy.minmax_direction_memo(board, 0, -float('inf'), float('inf'), True)
    fin = time.clock()
    
    logic.slide(direction, board)
    strategy.choose_new_tile(None, board)
    
    tps_memo += (fin - debut)

print("temps moyen alpha =" + str(tps_alpha/TESTS) + " ")
print("temps moyen memoi =" + str(tps_memo/TESTS) + " ")
