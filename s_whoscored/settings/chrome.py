import logging

from s_whoscored.settings import EXTENSIONS

EXTENSIONS.update({"s_whoscored.extensions.chrome.ChromeExtension": 0})

BROWSER_LEVEL = logging.WARNING
WS_P_LOG_LEVEL = logging.WARNING
WS_C_LOG_LEVEL = logging.WARNING
