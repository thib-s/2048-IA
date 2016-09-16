# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:32:23 2015
Module de test des Fonctions du fichier strategy.py
@author: Valentin Levesy, Thibaut Boissin
"""
#imports###################################################################

import random
import strategy
import score_utility
import logic

#FONCTIONS#################################################################

def start_test(name):
    print("*********** start test: " + name + " *******************")

#TESTS#####################################################################

start_test('test 1')
board = logic.init([
    [16, 2,  2,  2],
    [ 4, 4,  0,  0],
    [ 8, 8,  2,  4],
    [ 0, 0,  0,  0],
])
#assert strategy.score_corner(board) == 150

start_test('test 2')
board = logic.init([
    [  0, 16, 16,  2],
    [  0, 32,128,  4],
    [  2,  0, 64, 64],
    [ 16,  4, 32,  0]
])
#assert strategy.score_corner(board) == 39

start_test('test slide')
board = logic.init([
    [  0, 16, 16,  2],
    [  0, 32,128,  4],
    [  2,  0, 64, 64],
    [ 16,  4, 32,  0]
])
print(score_utility.slide_score(logic.RIGHT, board))# == 128