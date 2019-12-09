"""
httpcache configuration for this spider
"""
from typing import Dict, List

from s_whoscored.settings import DOWNLOADER_MIDDLEWARES, get_env

DOWNLOADER_MIDDLEWARES.update(
    {
        "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": None,
        "scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware": 900,
    }
)

HTTPCACHE_ENABLED: bool = True
HTTPCACHE_IGNORE_HTTP_CODES: List[int] = [301, 302, 500, 503]

HTTPCACHE_STORAGE: str = "scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage"

HTTPCACHE_MONGODB_HOST: str = get_env(
    "S_WHOSCORED_HTTPCACHE_MONGODB_HOST", default="127.0.0.1"
)
HTTPCACHE_MONGODB_PORT: int = int(
    get_env("S_WHOSCORED_HTTPCACHE_MONGODB_PORT", default=27017)
)

HTTPCACHE_MONGODB_USERNAME: str = get_env(
    "S_WHOSCORED_HTTPCACHE_MONGODB_USERNAME", default="root"
)
HTTPCACHE_MONGODB_PASSWORD: str = get_env(
    "S_WHOSCORED_HTTPCACHE_MONGODB_PASSWORD", default="xxxxxxxx"
)
HTTPCACHE_MONGODB_AUTH_DB: str = get_env(
    "S_WHOSCORED_HTTPCACHE_MONGODB_AUTH_DB", default="admin"
)

HTTPCACHE_MONGODB_CONNECTION_POOL_KWARGS: Dict = {}

HTTPCACHE_MONGODB_DB: str = get_env(
    "S_WHOSCORED_HTTPCACHE_MONGODB_DB", default="cache_storage"
)
HTTPCACHE_MONGODB_COLL: str = get_env(
    "S_WHOSCORED_HTTPCACHE_MONGODB_COLL", default="cache"
)
