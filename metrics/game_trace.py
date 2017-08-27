import logging
import time
import tools.PickleIO as pkio
from gamelogic import logic


class GameTrace:
    """
    basic class that allow to create game trace dict and to save it to a file

    each game is indexed with the timestamp of it's beginning
    each game consist in a list of tuple containing:
        - the board
        - the score
        - the choosen direction


    """
    def __init__(self, fileName):
        self.fileName = fileName
        try:
            obj = pkio.load_obj(fileName)
            logging.info("successfully loaded trace file " + str(fileName))
            self.gameTraceDict = obj
        except:
            logging.warn("unable to load data, create new one & saving it to " + str(fileName))
            self.gameTraceDict = dict()
            self.saveToDisk()

    def generateId(self):
        logging.debug("game id:" + str(time.time()))
        return time.time()

    def saveToDisk(self):
        logging.debug("saved gametrace to disk!")
        pkio.save_obj(self.gameTraceDict, self.fileName)

    def getGame(self, gameIndex):
        return self.gameTraceDict[gameIndex]

    def setGame(self, gameIndex, moveList):
        self.gameTraceDict[gameIndex] = moveList

    def addMove(self, gameIndex, boardBeforeComputer, boardComputer, score, direction):
        cpboardBeforeComputer = logic.copy_board(boardBeforeComputer)
        cpboardComputer = logic.copy_board(boardComputer)
        logging.debug("saving " + str(direction) + " to game " + str(gameIndex))
        try:
            game = self.getGame(gameIndex)
        except:
            logging.debug("no game with such id found, creating new dict")
            game = list()
        game.append({
            'board': cpboardComputer,
            'boardBeforeComputer': cpboardBeforeComputer,
            'score': score,
            'direction': direction
        })
        self.setGame(gameIndex, game)

    def getValues(self):
        return self.gameTraceDict.values()
