# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:57:16 2015

@author:  Valentin Levesy, Thibaut Boissin
"""

#imports###################################################################
import datetime
from scipy.optimize import minimize

import cma

from pybrain.optimization import CMAES
from pyevolve import G1DList, Mutators, Initializators, GSimpleGA, Consts

import logic
import strategy
import numpy as np





#CONFIGURATION#############################################################

OPTIMIZER = "pyevolve"
SAVE_RESULTS = False
dir_strat = 'brain'
scr_strat = 'ecart'
til_strat = 'random'
N = 5
NB_COUPS_MAX = 1000
MAX_ITER = 100
OUT_FOLDER = "opti_results/"

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
    if OPTIMIZER == "pyevolve":
        vect = genome.genomeList
    else:
        vect = genome#map(lambda x: x / PRECISION, genome.genomeList)
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
    return 1/moyenne(result)


#SCIPY_MINIMIZE################################################################

def scipy_minimize():
    #bnd = np.array([0, 1])
    #for i in range(len(strategy.WEIGHTS)-1):
    #    np.append(bnd, [0, 1])#bounds=bnd
    res = minimize(play_game, strategy.WEIGHTS, options={'disp': True})
    print(res)
    if SAVE_RESULTS:
        dt = str(datetime.datetime.now())
        name = OUT_FOLDER + "best_" + dt
        np.save(name, res.x)
        np.save("best", res.x)


#PYBRAIN_CMA####################################################################
def pybrain_cma(maxEval = 100):
    l = CMAES(play_game, strategy.WEIGHTS)
    l.minimize = True
    l.maxEvaluations = maxEval
    res = l.learn()
    print res
    if SAVE_RESULTS:
        dt = str(datetime.datetime.now())
        name = OUT_FOLDER + "pybraincma_" + dt
        np.save(name, res[0])
        np.save("best", res[0])


#CMA############################################################################

def cma_lib():
    res = cma.fmin(play_game, strategy.WEIGHTS, 0.25, {'maxiter': MAX_ITER}, restart_from_best=True)
    print("best:" + str(res[0]))  # best evaluated solution
    print("mean:" + str(res[5]))  # mean solution, presumably better with noise
    if SAVE_RESULTS:
        fig = cma.plot()
        dt = str(datetime.datetime.now())
        name = OUT_FOLDER + "cma_info_" + dt + ".png"
        cma.savefig(name)
        name = OUT_FOLDER + "cma_best_" + dt
        np.save(name, np.asarray(res[0]))
        np.save("best", res[0])
        name = OUT_FOLDER + "cma_avg_" + dt
        np.save(name, np.asarray(res[5]))


#PYEVOLVE########################################################################

def pyevolve():
    strategy.brain_init()
    genome = G1DList.G1DList(len(strategy.NET.params))
    genome.setParams(rangemin=0.0, rangemax=1.0)
    # Change the initializator to Real values
    genome.initializator.set(Initializators.G1DListInitializatorReal)
    # Change the mutator to Gaussian Mutator
    genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
    genome.evaluator.set(play_game)
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setMultiProcessing(False)
    ga.setGenerations(MAX_ITER)
    ga.setMutationRate(0.05)
    ga.setPopulationSize(200)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.evolve(freq_stats=1)
    res = np.asarray(ga.bestIndividual().genomeList)
    print res
    if SAVE_RESULTS:
        dt = str(datetime.datetime.now())
        name = OUT_FOLDER + "pyevolve_" + dt
        np.save(name, res[0])
        np.save("best", res[0])



#RESULTS#########################################################################

#dt = str(datetime.datetime.now())
#name = OUT_FOLDER+"best_"+dt
#res = np.asarray(ga.bestIndividual().genomeList)#map(lambda x: x / PRECISION,np.asarray(ga.bestIndividual().genomeList))
#print res
#np.save(name, res[0])
#np.save("best", res[0])

##################################################################################

def optimize(optimizer):
    if optimizer == "scipy_minimize":
        scipy_minimize()
    elif optimizer == "pybrain_cma":
        pybrain_cma()
    elif optimizer == "cma":
        cma_lib()
    elif optimizer == "pyevolve":
        pyevolve()
    else:
        raise ValueError('No such optimizer', optimizer)

#RUN SCRIPT########################################################################

strategy.DIRECTION_STRATEGY = dir_strat
strategy.NEW_TILE_STRATEGY = til_strat
strategy.SCORE_FUNCTION = scr_strat

optimize(OPTIMIZER)
