import logging

from datasets import ComputeBoardScores as compute
from metrics import game_trace as gt

logging.basicConfig(level=logging.DEBUG)

gameTrace = gt.GameTrace('gametrace')
logging.info("gametrace loaded, size " + str(len(gameTrace.getValues())))

compute.computeScoreDataset(gameTrace)
