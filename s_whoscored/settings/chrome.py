import logging

from s_whoscored.settings import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update(
    {"s_whoscored.downloadermiddlewares.chrome.ChromeMiddleware": 999}
)

BROWSER_LEVEL = logging.WARNING
WS_P_LOG_LEVEL = logging.WARNING
WS_C_LOG_LEVEL = logging.WARNING
