"""
Configure pyppeteer in this spider

 * remove websocket timeout restriction
 * set pyppeteer logger level to WARNING
"""
import logging

import pyppeteer.connection
from websockets.client import logger as WSCLogger
from websockets.protocol import logger as WSPLogger

from s_whoscored.settings import EXTENSIONS

EXTENSIONS.update({"s_whoscored.extensions.pyppeteer.Pyppeteer": 0})

original_method = pyppeteer.connection.websockets.client.connect


def new_method(*args, **kwargs):
    """
    Remove websocket timeout restriction in pyppeteer
    :param args:
    :param kwargs:
    :return:
    """
    kwargs["ping_interval"] = None
    kwargs["ping_timeout"] = None
    return original_method(*args, **kwargs)


pyppeteer.connection.websockets.client.connect = new_method

PYPPETEER_LOG_LEVEL = logging.WARNING

WSCLogger.setLevel(PYPPETEER_LOG_LEVEL)
WSPLogger.setLevel(PYPPETEER_LOG_LEVEL)
