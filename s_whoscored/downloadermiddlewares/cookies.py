"""
The customized cookies downloader middleware

"""
from __future__ import annotations

import logging
from typing import Optional

from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from scrapy.settings import Settings
from scrapy.spiders import Spider
from scrapy_cookies.downloadermiddlewares.cookies import CookiesMiddleware as CM_Origin

from s_whoscored.crawler import Crawler
from s_whoscored.downloadermiddlewares import as_deferred


class CookiesMiddleware(CM_Origin):
    """
    The customized cookies downloader middleware
    """

    def __init__(self, settings: Settings):
        super(CookiesMiddleware, self).__init__(settings=settings)
        self.browser: Optional[Browser] = None

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> CookiesMiddleware:
        return super().from_crawler(crawler=crawler)

    @as_deferred
    async def spider_opened(self, signal: object, sender: Crawler, spider: Spider):
        super(CookiesMiddleware, self).spider_opened(spider=spider)
        self.browser = await launch(headless=False, logLevel=logging.WARNING)

    @as_deferred
    async def spider_closed(  # pylint: disable=bad-continuation
        self, signal: object, sender: Crawler, reason: str, spider: Spider
    ):
        super(CookiesMiddleware, self).spider_closed(spider=spider)
        await self.browser.close()
