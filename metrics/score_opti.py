# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:57:16 2015

@author:  Valentin Levesy, Thibaut Boissin
"""

#imports###################################################################

import cma
from gamelogic import logic
# import score_utility
import numpy as np

from gamelogic import strategy

#CONFIGURATION#############################################################

dir_strat = 'score'
scr_strat = 'ecart'
til_strat = 'random'
N = 5



#FONCTIONS#################################################################

def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)
    
def scoring(board):
    result = 0
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            result = result + (board[x][y]-1)*(2**board[x][y])
    return result

#TESTS#####################################################################

strategy.DIRECTION_STRATEGY = dir_strat
strategy.NEW_TILE_STRATEGY = til_strat
strategy.SCORE_FUNCTION = scr_strat

def play_game(vect):
    result = []
    n = 0
    while (n < N):
        strategy.set_random_seed(n)
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
        result.append(scoring(board))
    return (1/moyenne(result))


x0 = np.array([1,10,600,40,35,0.5])
#res = minimize(play_game, x0, method='nelder-mead',options={'xtol': 1e-3, 'disp': True})
#print(res.x)
res = cma.fmin(play_game, [0.5,0.5,0.5,0.5,0.5,0.5], 0.25,{'maxiter':200})
#print(res.x)
print("best:"+ str(res[0]))  # best evaluated solution
print("mean:"+str(res[5]))  # mean solution, presumably better with noise
cma.plot()

#(4_w,9)-aCMA-ES (mu_w=2.8,w_1=49%) in dimension 6 (seed=1115866, Sun Oct  9 00:59:52 2016)
#Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
#    1      9 1.786735277301315e-04 1.0e+00 2.33e-01  2e-01  2e-01 0:9.0
#    2     18 1.787501787501788e-04 1.1e+00 2.36e-01  2e-01  2e-01 0:17.4
#    3     27 1.570549063952758e-04 1.3e+00 2.33e-01  2e-01  2e-01 0:27.4
#   98    882 1.239464551313832e-04 8.3e+00 9.11e-03  2e-03  6e-03 22:9.6
#termination on tolfunhist=1e-12 (Sun Oct  9 01:22:03 2016)
#termination on flat fitness: please (re)consider how to compute the fitness more elaborate=None (Sun Oct  9 01:22:03 2016)
#final/bestever f-value = 1.239465e-04 1.179802e-04
#incumbent solution: [0.24379714007253764, 0.61585169607123424, 0.1590607462715867, 0.91880279881906746, 0.50550968042275379, 0.60324280431778998]
#std deviation: [0.0023499163521791687, 0.0055933127336112651, 0.0053824646099032017, 0.0058865494903427452, 0.0040230822625523296, 0.0045842979620687764]
#best:[ 0.21088312  0.58642133  0.25750207  0.99326141  0.54198695  0.50119816]
#mean:[ 0.24379714  0.6158517   0.15906075  0.9188028   0.50550968  0.6032428 ]


#(4_w,9)-aCMA-ES (mu_w=2.8,w_1=49%) in dimension 6 (seed=1034916, Sun Oct  9 00:49:49 2016)
#Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
#    1      9 1.531862745098039e-04 1.0e+00 8.69e-02  8e-02  9e-02 0:1.6
#    2     18 2.883506343713956e-04 1.1e+00 8.07e-02  8e-02  8e-02 0:3.1
#    3     27 2.896871378910776e-04 1.2e+00 7.03e-02  6e-02  7e-02 0:4.5
#   69    621 1.361655773420479e-04 9.9e+00 2.82e-02  2e-02  3e-02 2:34.2
#termination on tolfunhist=1e-12 (Sun Oct  9 00:52:23 2016)
#termination on flat fitness: please (re)consider how to compute the fitness more elaborate=None (Sun Oct  9 00:52:23 2016)
#final/bestever f-value = 1.361656e-04 1.361656e-04
#incumbent solution: [0.82505222235473397, 1.0429688315692467, 0.97126637160067952, 1.108443973591495, 0.74422725886140151, 1.0744414482041749]
#std deviation: [0.018541360600147879, 0.027815066220323835, 0.019941185600626452, 0.022594648164259611, 0.027990572918995548, 0.021738727096424909]
#best:[ 0.86666572  0.89650868  1.09492106  1.20565786  0.8662517   1.10302375]
#mean:[ 0.82505222  1.04296883  0.97126637  1.10844397  0.74422726  1.07444145]


#(4_w,9)-aCMA-ES (mu_w=2.8,w_1=49%) in dimension 6 (seed=1111631, Sun Oct  9 00:39:07 2016)
#Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
#    1      9 1.816860465116279e-04 1.0e+00 1.79e+00  2e+00  2e+00 0:1.3
#    2     18 1.043405676126878e-04 1.1e+00 1.66e+00  2e+00  2e+00 0:3.4
#    3     27 6.340349987319300e-05 1.2e+00 1.75e+00  2e+00  2e+00 0:7.0
#  100    900 6.041565973900435e-05 1.4e+01 2.91e-01  6e-02  3e-01 8:1.9
#termination on tolfunhist=1e-12 (Sun Oct  9 00:47:09 2016)
#termination on flat fitness: please (re)consider how to compute the fitness more elaborate=None (Sun Oct  9 00:47:09 2016)
#termination on tolfun=1e-11 (Sun Oct  9 00:47:09 2016)
#final/bestever f-value = 6.041566e-05 6.016847e-05
#incumbent solution: [4.487314987345882, 13.639094728204505, 600.14906557161805, 38.971890331496567, 28.910373223720782, 5.3122362541603962]
#std deviation: [0.057659506318215516, 0.25539206277816606, 0.1217669741150182, 0.18424596116896513, 0.14250977892808103, 0.065761604956980621]
#best:[   5.6630379     7.40627988  599.70060533   42.66285499   30.66819842
#    3.14889657]
#mean:[   4.48731499   13.63909473  600.14906557   38.97189033   28.91037322
#    5.31223625]


#
#(4_w,9)-aCMA-ES (mu_w=2.8,w_1=49%) in dimension 6 (seed=1104342, Sun Oct  9 00:25:32 2016)
#Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
#    1      9 1.380452788514633e-04 1.0e+00 2.24e+01  2e+01  2e+01 0:0.9
#    2     18 1.470588235294118e-04 1.1e+00 2.27e+01  2e+01  2e+01 0:2.8
#    3     27 9.765625000000001e-05 1.3e+00 2.24e+01  2e+01  2e+01 0:4.5
#  100    900 6.485084306095979e-05 1.1e+01 7.12e-01  8e-02  6e-01 7:0.3
#  102    918 6.485084306095979e-05 1.0e+01 7.74e-01  9e-02  6e-01 7:11.6
#termination on flat fitness: please (re)consider how to compute the fitness more elaborate=None (Sun Oct  9 00:32:44 2016)
#termination on tolfunhist=1e-12 (Sun Oct  9 00:32:44 2016)
#final/bestever f-value = 6.485084e-05 5.965163e-05
#incumbent solution: [36.965462597447484, 44.757401347430026, 563.37865625262293, 87.271246753058435, 58.523440700047999, 9.4427816236531132]
#std deviation: [0.23631908277805505, 0.61086784690430096, 0.25344542287592392, 0.63627076126643289, 0.46788578543839043, 0.086942689466599332]
#best:[  34.41149018   -9.4324723   571.31465813   69.82992158   39.22924969
#   13.49052569]
#mean:[  36.9654626    44.75740135  563.37865625   87.27124675   58.5234407
#    9.44278162]


#(4_w,9)-aCMA-ES (mu_w=2.8,w_1=49%) in dimension 6 (seed=1073802, Sat Oct  8 23:22:48 2016)
#Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
#    1      9 1.231527093596059e-04 1.0e+00 2.76e+01  3e+01  3e+01 0:2.1
#    2     18 1.150218541522889e-04 1.4e+00 2.81e+01  3e+01  3e+01 0:5.6
#    3     27 1.591343093570974e-04 1.4e+00 2.66e+01  2e+01  3e+01 0:9.2
#  100    900 6.982265046781176e-05 2.5e+01 2.69e+01  6e+00  4e+01 9:43.1
#  145   1305 6.620762711864407e-05 1.1e+02 6.49e+00  7e-01  2e+01 17:16.8
#termination on tolfun=1e-11 (Sat Oct  8 23:40:05 2016)
#termination on tolfunhist=1e-12 (Sat Oct  8 23:40:05 2016)
#termination on flat fitness: please (re)consider how to compute the fitness more elaborate=None (Sat Oct  8 23:40:05 2016)
#final/bestever f-value = 6.620763e-05 5.566689e-05
#incumbent solution: [47.163933434050001, 37.059649768204814, 1005.8582246825005, 238.03858999798092, -20.466133240700227, 32.259843081820961]
#std deviation: [1.1303575412923046, 3.5965369247643362, 15.240173115942543, 5.5874288973040578, 1.8468239271650413, 0.73064016868132642]