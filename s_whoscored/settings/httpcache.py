"""
httpcache configuration for this spider
"""
from typing import Dict, List

from s_whoscored.settings import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update(
    {
        "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": None,
        "scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware": 900,
    }
)

HTTPCACHE_ENABLED: bool = True
HTTPCACHE_IGNORE_HTTP_CODES: List[int] = [301, 302, 500, 503]

HTTPCACHE_STORAGE: str = "scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage"

HTTPCACHE_MONGODB_HOST: str = "127.0.0.1"
HTTPCACHE_MONGODB_PORT: int = 27017

HTTPCACHE_MONGODB_USERNAME: str = "root"
HTTPCACHE_MONGODB_PASSWORD: str = "xxxxxxxx"
HTTPCACHE_MONGODB_AUTH_DB: str = "admin"

HTTPCACHE_MONGODB_CONNECTION_POOL_KWARGS: Dict = {}

HTTPCACHE_MONGODB_DB: str = "cache_storage"
HTTPCACHE_MONGODB_COLL: str = "cache"
