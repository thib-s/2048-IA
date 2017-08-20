from networkx import DiGraph

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
    # compute the dataset from the graph
    return extractScores(graph)


def addMoveToGraph(move, graph):
    """
    extract order information from a move
    :param move: the move to extract order from
    :param graph:  the graph to inflate
    :return:  the inflated  graph
    """
    # get infos from move
    board = move.get('board')
    bestDirection = move.get('direction')
    nextBoards = dict()
    # compute all available directions and add associated node
    possibleMoves = logic.possible_moves(board)
    for direction in possibleMoves:
        nextBoard = logic.copy_board(board)
        nextBoards[direction] = Normalizer.normalize(logic.slide(direction, nextBoard))
        graph.add_node(nextBoards[direction])
    # add edges to modelize order
    for direction in possibleMoves:
        if direction != bestDirection:
            graph.add_edge(nextBoards[bestDirection], nextBoards[direction])
    return graph


def computeGraph(gameTrace):
    """
    compute the directed graph that modelize the partial order between boards
    :param gameTrace used to compute the graph
    :return the DiGraph object of partial order
    """
    graph = DiGraph()
    gameList = gameTrace.getValues()
    for game in gameList:
        for move in game:
            addMoveToGraph(move, graph)


def extractScores(partialOrder):
    """
    compute the score associated to each normalized board using the graph
    :param partialOrder the digraph used to compute scores
    :return the dataset as a dict
    """
    # step 1 : find all sources of the graph and compute its weight
    # step 2 : compute the score of each node and put it in the dataset
    pass
