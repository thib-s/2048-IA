# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:57:16 2015

@author:  Valentin Levesy, Thibaut Boissin
"""

#imports###################################################################
import datetime

import cma
import time

from pybrain.optimization import NelderMead, CMAES

import logic
import strategy
import numpy as np





#CONFIGURATION#############################################################

dir_strat = 'brain'
scr_strat = 'ecart'
til_strat = 'random'
N = 5
NB_COUPS_MAX = 1000
MAX_ITER = 100
OUT_FOLDER = "opti_results/"


strategy.DIRECTION_STRATEGY = dir_strat
strategy.NEW_TILE_STRATEGY = til_strat
strategy.SCORE_FUNCTION = scr_strat


#FONCTIONS#################################################################

def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)
    
def scoring(board):
    result = 0
    for x in range(logic.SIZE):
        for y in range(logic.SIZE):
            result = result + (board[x][y]-1)*(2**board[x][y])
    return np.log(result)

def play_game(genome):
    result = []
    n = 0
    vect = genome#genome.genomeList#map(lambda x: x / PRECISION, genome.genomeList)
    strategy.BRAIN_INIT = False
    strategy.set_brain_weights(vect)
    while (n < N):
        strategy.BRAIN_INIT = False
        strategy.set_brain_weights(vect)
        #strategy.set_random_seed(n)
        board = logic.empty_board()
        state = 'new_tile'
        nb_coup = 0
        while state != 'gameover' and nb_coup<=NB_COUPS_MAX:
            if state == 'new_tile':
                logic.computer_move(strategy.choose_new_tile(None, board), board)
                state = 'direction'
            elif state == 'direction':
                logic.slide(strategy.brain_choose_direction(board), board)
                nb_coup += 1
                state = 'new_tile'
            if logic.game_over(board):
                state = 'gameover'
        n += 1
        result.append(scoring(board))
    return moyenne(result)


#SCIPY_MINIMIZE################################################################

#x0 = np.array([1,10,600,40,35,0.5])
#res = minimize(play_game, strategy.WEIGHTS, bounds=(0, 1), method='nelder-mead', options={'xtol': 1e-3, 'disp': True})
#print(res.x)


#PYBRAIN_CMA####################################################################

#l = CMAES(play_game, strategy.WEIGHTS)
#l.maxEvaluations = 10000
#res = l.learn()


#CMA############################################################################

res = cma.fmin(play_game, strategy.WEIGHTS, 0.25,{'maxiter':MAX_ITER},restart_from_best=True)
print("best:"+ str(res[0]))  # best evaluated solution
print("mean:"+str(res[5]))  # mean solution, presumably better with noise
fig = cma.plot()
dt = str(datetime.datetime.now())
name = OUT_FOLDER+"opti_"+dt+".png"
cma.savefig(name)
name = OUT_FOLDER+"best_"+dt
np.save(name,np.asarray(res[0]))
np.save("best", res[0])
name = OUT_FOLDER+"avg_"+dt
np.save(name,np.asarray(res[5]))


#PYEVOLVE########################################################################

#strategy.brain_init()
#genome = G1DList.G1DList(len(strategy.NET.params))
#genome.setParams(rangemin=0.0, rangemax=1.0)
# Change the initializator to Real values
#genome.initializator.set(Initializators.G1DListInitializatorReal)
# Change the mutator to Gaussian Mutator
#genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
#genome.evaluator.set(play_game)
#ga = GSimpleGA.GSimpleGA(genome)
#ga.setMultiProcessing(False)
#ga.setGenerations(100)
#ga.setMutationRate(0.05)
#ga.setPopulationSize(200)
#ga.evolve(freq_stats=1)


#RESULTS#########################################################################

#dt = str(datetime.datetime.now())
#name = OUT_FOLDER+"best_"+dt
#res = np.asarray(ga.bestIndividual().genomeList)#map(lambda x: x / PRECISION,np.asarray(ga.bestIndividual().genomeList))
#print res
#np.save(name, res[0])
#np.save("best", res[0])
