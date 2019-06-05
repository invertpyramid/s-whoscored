"""
httpcache configuration for this spider
"""
from s_whoscored.settings import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update(
    {
        "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": None,
        "scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware": 900,
    }
)

HTTPCACHE_ENABLED = True
HTTPCACHE_IGNORE_HTTP_CODES = [301, 302, 500, 503]

HTTPCACHE_STORAGE = "scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage"

HTTPCACHE_MONGODB_HOST = "127.0.0.1"
HTTPCACHE_MONGODB_PORT = 27019

HTTPCACHE_MONGODB_USERNAME = "root"
HTTPCACHE_MONGODB_PASSWORD = "xxxxxxxx"
HTTPCACHE_MONGODB_AUTH_DB = "admin"

HTTPCACHE_MONGODB_CONNECTION_POOL_KWARGS = {}

HTTPCACHE_MONGODB_DB = "cache_storage"
HTTPCACHE_MONGODB_COLL = "cache"
