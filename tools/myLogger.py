# -*- coding: utf-8 -*-

import logging
import time

FILE = 'logs/'
LEVEL = logging.DEBUG


def configure_logger_prod():
    global LEVEL
    logging.basicConfig(filename=FILE+str(time.time())+'.log', level=LEVEL)


def configure_logger_warning():
    logging.disable(logging.WARNING)


def configure_logger_info():
    logging.basicConfig(level=logging.INFO)

