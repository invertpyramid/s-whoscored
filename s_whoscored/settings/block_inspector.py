"""
Block inspector middleware configuration
"""
from s_whoscored.settings import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update(
    {"s_whoscored.downloadermiddlewares.block_inspector.BlockInspectorMiddleware": 950,}
)
