"""
middlewares configuration for this spider
"""
from s_whoscored.settings import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update(
    {
        "scrapy.downloadermiddlewares.cookies.CookiesMiddleware": None,
        "s_whoscored.downloadermiddlewares.cookies.CookiesMiddleware": 700,
    }
)

COOKIES_STORAGE: str = "scrapy_cookies.storage.mongo.MongoStorage"
COOKIES_MONGO_MONGOCLIENT_HOST: str = "127.0.0.1"
COOKIES_MONGO_MONGOCLIENT_PORT: int = 27020
