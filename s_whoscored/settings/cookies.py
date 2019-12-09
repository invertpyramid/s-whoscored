"""
middlewares configuration for this spider
"""
from s_whoscored.settings import DOWNLOADER_MIDDLEWARES, get_env

DOWNLOADER_MIDDLEWARES.update(
    {
        "scrapy.downloadermiddlewares.cookies.CookiesMiddleware": None,
        "s_whoscored.downloadermiddlewares.cookies.CookiesMiddleware": 700,
    }
)

COOKIES_STORAGE: str = "scrapy_cookies.storage.mongo.MongoStorage"

COOKIES_MONGO_MONGOCLIENT_HOST: str = get_env(
    "S_WHOSCORED_COOKIES_MONGO_MONGOCLIENT_HOST", default="127.0.0.1"
)
COOKIES_MONGO_MONGOCLIENT_PORT: int = int(
    get_env("S_WHOSCORED_COOKIES_MONGO_MONGOCLIENT_PORT", default=27017)
)

COOKIES_MONGO_MONGOCLIENT_KWARGS = {
    "username": "root",
    "password": "xxxxxxxx",
    "authSource": "admin",
    "authMechanism": "SCRAM-SHA-1",
}
