# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:57:16 2015

@author:  Valentin Levesy, Thibaut Boissin
"""

#imports###################################################################

import logic
import strategy
import score_utility
from scipy.optimize import minimize
import numpy as np



#CONFIGURATION#############################################################

dir_strat = 'score'
scr_strat = 'corner_edge'
til_strat = 'random'
N = 100



#FONCTIONS#################################################################

def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)

#TESTS#####################################################################

strategy.DIRECTION_STRATEGY = dir_strat
strategy.NEW_TILE_STRATEGY = til_strat
strategy.SCORE_FUNCTION = scr_strat

def play_game(vect):
    result = []
    n = 0
    while (n < N):
        board = logic.empty_board()
        state = 'new_tile'
        nb_coup = 0
        while state != 'gameover':
            if state == 'new_tile':
                logic.computer_move(strategy.choose_new_tile(None, board), board)
                state = 'direction'
            elif state == 'direction':
                strategy.V = vect
                logic.slide(strategy.score_choose_direction(board), board)
                nb_coup += 1
                state = 'new_tile'
            if logic.game_over(board):
                state = 'gameover'
        n += 1
        result.append(score_utility.best_tile(board)[2])
    return -moyenne(result)


x0 = np.array([1,10,600,40,35])
res = minimize(play_game, x0, method='nelder-mead',options={'xtol': 1e-1, 'disp': True})
print(res.x)
#res = cma.fmin(play_game, [1,10,600,40,35,0.5], 25,{'maxiter':200})
#res[0]  # best evaluated solution
#res[5]  # mean solution, presumably better with noise

#
#(4_w,9)-aCMA-ES (mu_w=2.8,w_1=49%) in dimension 6 (seed=683533, Tue Apr 21 20:17:17 2015)
#Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
#    1      9 -8.330000000000000e+00 1.0e+00 2.39e+01  2e+01  2e+01 18:7.6
#    2     18 -8.199999999999999e+00 1.2e+00 2.43e+01  2e+01  3e+01 36:1.4
#    3     27 -8.260000000000000e+00 1.4e+00 2.19e+01  2e+01  2e+01 54:15.4
#    5     45 -8.210000000000001e+00 1.4e+00 2.17e+01  2e+01  2e+01 95:22.6
#termination on maxiter=5 (Tue Apr 21 21:54:59 2015)
#final/bestever f-value = -8.010000e+00 -8.330000e+00
#incumbent solution: [20.304416920589404, -20.579861571974654, 611.24798345561646, 81.850248879919675, 34.957490944894531, -2.4911345163166985]
#std deviation: [21.641431258822315, 22.05803486634963, 21.722251347965347, 21.48118729136311, 19.891883686775628, 19.945646929228335]


#
#(4_w,9)-aCMA-ES (mu_w=2.8,w_1=49%) in dimension 6 (seed=682949, Tue Apr 21 22:01:56 2015)
#Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
#    1      9 -9.000000000000000e+00 1.0e+00 2.27e+01  2e+01  2e+01 0:23.5
#    2     18 -9.000000000000000e+00 1.2e+00 2.29e+01  2e+01  2e+01 0:51.4
#    3     27 -8.500000000000000e+00 1.3e+00 2.41e+01  2e+01  3e+01 1:21.5
#  100    900 -9.500000000000000e+00 1.7e+01 2.68e+01  1e+01  4e+01 40:21.3
#  200   1800 -8.500000000000000e+00 5.2e+01 7.73e+00  4e+00  1e+01 74:29.8
#termination on maxiter=200 (Tue Apr 21 23:16:26 2015)
#final/bestever f-value = -7.500000e+00 -1.000000e+01
#incumbent solution: [-42.020677201534113, 8.1447277742361273, 573.23955867450718, 134.53070695046094, 49.563180610558149, -72.712984979858007]
#std deviation: [10.629499951895053, 4.8860136887642902, 4.8400315132616836, 4.0650609155714488, 7.5800176997793098, 3.8861104018630628]
