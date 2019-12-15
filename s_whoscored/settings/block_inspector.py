"""
Block inspector middleware configuration
"""
import logging

from s_whoscored.settings import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update(
    {
        "s_whoscored.downloadermiddlewares.block_inspector.BlockInspectorMiddleware": 950,
        "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 960,
    }
)

BROWSER_LEVEL = logging.WARNING
WS_C_LOG_LEVEL = logging.WARNING
WS_P_LOG_LEVEL = logging.WARNING
