import logging
import pyppeteer.connection
from websockets.protocol import logger as WSPLogger

original_method = pyppeteer.connection.websockets.client.connect


def new_method(*args, **kwargs):
    kwargs["ping_interval"] = None
    kwargs["ping_timeout"] = None
    return original_method(*args, **kwargs)


pyppeteer.connection.websockets.client.connect = new_method
WSPLogger.setLevel(logging.WARNING)
