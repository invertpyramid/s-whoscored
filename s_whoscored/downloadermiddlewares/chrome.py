"""
The middleware to operate Chrome Browser
"""
from __future__ import annotations

import logging
from typing import Optional

from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from scrapy.crawler import Crawler
from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.signals import spider_closed, spider_opened
from scrapy.spiders import Spider
from scrapy.statscollectors import StatsCollector
from websockets.client import logger as WS_C_Logger
from websockets.protocol import logger as WS_P_Logger

from s_whoscored.downloadermiddlewares import as_deferred
from s_whoscored.signals import response_blocked

logger = logging.getLogger(__name__)


class ChromeMiddleware:
    """
    The middleware to operate Chrome Browser
    """

    def __init__(self, crawler: Crawler):
        """

        :param crawler:
        :type crawler: Crawler
        """
        self.crawler: Crawler = crawler
        self.settings: Settings = crawler.settings
        self.stats: StatsCollector = crawler.stats

        self.browser: Optional[Browser] = None

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> ChromeMiddleware:
        """

        :param crawler:
        :type crawler: Crawler
        :return:
        :rtype: ChromeMiddleware
        """
        obj = cls(crawler)
        crawler.signals.connect(obj.spider_opened, spider_opened)
        crawler.signals.connect(obj.spider_closed, spider_closed)
        crawler.signals.connect(obj.visit_page, response_blocked)

        WS_C_Logger.setLevel(crawler.settings["WS_C_LOG_LEVEL"])
        WS_P_Logger.setLevel(crawler.settings["WS_P_LOG_LEVEL"])

        return obj

    @as_deferred
    async def spider_opened(
        self, sender: Crawler, signal: object, spider: Spider, *args, **kwargs
    ) -> None:
        """

        :param sender:
        :type sender: Crawler
        :param signal:
        :type signal: object
        :param spider:
        :type spider: Spider
        :return:
        :rtype: None
        """
        logger.info("The middleware chrome is up.")
        self.browser: Browser = await launch(
            headless=False, logLevel=self.settings["BROWSER_LEVEL"]
        )

    @as_deferred
    async def spider_closed(
        self, sender: Crawler, signal: object, spider: Spider, reason, *args, **kwargs
    ) -> None:
        """

        :param sender:
        :type sender: Crawler
        :param signal:
        :type signal: object
        :param spider:
        :type spider: Spider
        :param reason:
        :type reason:
        :return:
        :rtype: None
        """
        logger.info("The middleware chrome is down.")
        await self.browser.close()

    def visit_page(
        self,
        sender: Crawler,
        signal: object,
        spider: Spider,
        request: Request,
        response: Response,
        *args,
        **kwargs,
    ):
        """

        :param sender:
        :type sender: Crawler
        :param signal:
        :type signal: object
        :param spider:
        :type spider: Spider
        :param request:
        :type request: Request
        :param response:
        :type response: Response
        :return:
        :rtype:
        """
        self.stats.inc_value("chrome/visit_pages")
        logger.info("A page need to be visited by Chrome: %s", response.url)
