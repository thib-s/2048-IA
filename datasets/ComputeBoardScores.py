import logging
from networkx import DiGraph, draw, draw_spectral

from gamelogic import logic, Normalizer


def computeScoreDataset(gameTrace):
    """
    compute the score dataset from a gameTrace object
    :param gameTrace the set of saved games used to compute the dataset
    :return the dataset as a dict: 
            keys: str(board)
            value: associated score
    """
    # compute the graph of partial orders
    graph = computeGraph(gameTrace)
    # print debug messages
    debugGraph(graph)
    # compute the dataset from the graph
    return extractScores(graph)


def debugGraph(graph):
    """
    print debug infos about the created graph
    :param graph: the graph to analyse
    :return: nothing
    """
    logging.info("debugging partial order graph")
    logging.info("number of nodes in the ordering graph:" + str(graph.number_of_nodes()))
    logging.info("number of edges in the ordering graph:" + str(graph.number_of_edges()))
    if graph.number_of_selfloops()!=0:
        logging.warning(str(graph.number_of_selfloops())+" self loops found in graph")
    # dirty way to compute average of out degree
    sum = 0
    num_of_nodes = 0
    for node in graph.nodes():
        deg = graph.out_degree(node)
        sum = sum + deg
        if deg != 0:
            num_of_nodes = num_of_nodes + 1
            if graph.in_degree(node) > 0:
                logging.info("this sounds good!")
    logging.info("average of out degre of the graph:" + str(sum/num_of_nodes))
    print("in" + str(graph.in_degree(graph.nodes()).values()))
    print("out" + str(graph.out_degree(graph.nodes()).values()))
    print("nodes" + str(graph.nodes()))
    #draw_spectral(graph)

def getNextmove(move, game):
    nextIndex = game.index(move)
    if nextIndex < len(game):
        return game[nextIndex].get('boardBeforeComputer')
    else:
        return None


def addMoveToGraph(move, game, graph):
    """
    extract order information from a move
    :param move: the move to extract order from
    :param graph:  the graph to inflate
    :return:  the inflated  graph
    """
    # get infos from move
    board = move.get('board')
    bestDirection = move.get('direction')
    # step 2 compute leafs
    nextBoards = dict()
    # compute all available directions and add associated node
    possibleMoves = logic.possible_moves(board)
    for direction in possibleMoves:
        nextBoard = logic.copy_board(board)
        logic.slide(direction, nextBoard)
        nextBoards[direction] = Normalizer.normalize(nextBoard)
        # graph.add_node(str(nextBoards[direction]))
    # add edges to modelize order
    bestBoard = Normalizer.normalize(move.get('boardBeforeComputer'))
    for direction in possibleMoves:
        if direction != bestDirection:
            graph.add_edge(str(bestBoard), str(nextBoards[direction]))
    return graph


def computeGraph(gameTrace):
    """
    compute the directed graph that modelize the partial order between boards
    :param gameTrace used to compute the graph
    :return the DiGraph object of partial order
    """
    graph = DiGraph()
    gameList = gameTrace.getValues()
    logging.info("loaded gametrace, size:" + str(len(gameList)))
    for game in gameList:
        logging.info("loading next game, size:" + str(len(game)))
        for move in game:
            graph = addMoveToGraph(move, game, graph)
    return graph


def extractScores(partialOrder):
    """
    compute the score associated to each normalized board using the graph
    :param partialOrder the digraph used to compute scores
    :return the dataset as a dict
    """
    # step 1 : find all sources of the graph and compute its weight
    # step 2 : compute the score of each node and put it in the dataset
    pass
