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
#CONFIGURATION#############################################################

TESTS = 100

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

start_test('Seuls droite/gauche possible')
board = logic.init([
    [2,  4,  8, 16],
    [4,  8, 16, 32],
    [8, 16,  8,  4],
    [16, 8, 32, 32],
])
#la droite est prioritaire sur la gauche
assert strategy.priority_choose_direction(board) == logic.RIGHT

start_test('Seuls droite/bas possible')
board = logic.init([
    [2,  4,  8, 16],
    [4,  8, 16,  8],
    [8, 16,  8, 32],
    [16, 8,  4,  0],
])
#la droite est prioritaire sur lle bas
assert strategy.priority_choose_direction(board) == logic.RIGHT


start_test('Seuls droite/bas possible')
board = logic.init([
    [2,  4,  8, 16],
    [4,  8, 16,  8],
    [8, 16,  8, 32],
    [16, 8,  4,  0],
])
#la droite est prioritaire sur le bas
assert strategy.priority_choose_direction(board) == logic.RIGHT

start_test('Seuls haut/bas possible')
board = logic.init([
    [2,  4,  8, 16],
    [4,  8, 16,  8],
    [8, 16,  8, 32],
    [16, 8,  4, 32],
])
#le bas est prioritaire sur le haut
assert strategy.priority_choose_direction(board) == logic.DOWN

#MEGA-TEST#
#on prends beaucoup de tableaux aleatoires et on les teste
start_test('tests sur un grand nombre de board aleatoires')
for i in range(TESTS):
    board = random_board()
    directions = logic.possible_moves(board)
    if logic.RIGHT in directions == True:
        assert strategy.priority_choose_direction(board) == logic.RIGHT
    elif logic.DOWN in directions == True:
        assert strategy.priority_choose_direction(board) == logic.DOWN
    if logic.LEFT in directions == True:
        assert strategy.priority_choose_direction(board) == logic.LEFT
    if logic.UP in directions == True:
        assert strategy.priority_choose_direction(board) == logic.UP

print()
print("    function priority_choose_direction seems to be correct")
print()

start_test('cas le haut/bas sont mieux')
board = logic.init([
    [ 2, 4,  0,  0],
    [ 2, 4,  0,  0],
    [ 0, 0,  0,  0],
    [ 0, 0,  0,  0],
])
#le haut est prioritaire sur le bas
assert strategy.score_choose_direction(board) == logic.UP

start_test('cas le gauche/droite sont mieux')
board = logic.init([
    [ 2, 2,  0,  0],
    [ 4, 4,  0,  0],
    [ 0, 0,  0,  0],
    [ 0, 0,  0,  0],
])
assert strategy.score_choose_direction(board) == logic.LEFT

print()
print("    function score_choose_direction seems to be correct")
print()