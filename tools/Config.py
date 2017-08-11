import logging

import tools.PickleIO as pkio

"""
basic class that allow to create config dict and to save it to a file
"""


class Config:
    """
    create a config object
    :param fileName, the name of the config file, if the file does not exist,
           it will be created with defaultConfDict in it
    :param defaultConfDict, the default configuration dictionary to use if the file does not exist
    """

    def __init__(self, fileName, defaultConfDict):
        self.fileName = fileName
        try:
            obj = pkio.load_obj(fileName)
            logging.info("successfully loaded config file " + str(fileName))
            self.configDict = obj
        except:
            logging.error("unable to load conf, switching to default & saving it to " + str(fileName))
            self.configDict = defaultConfDict
            self.saveConfig()

    def getAttr(self, key):
        return self.configDict[key]

    def setAttr(self, key, value):
        self.configDict[key] = value

    def loadDict(self, dict):
        self.configDict = dict

    def saveConfig(self):
        pkio.save_obj(self.configDict, self.fileName)
