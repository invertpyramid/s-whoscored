"""
The middleware to operate Chrome Browser
"""
from __future__ import annotations

import logging

from scrapy.crawler import Crawler
from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.signals import spider_closed, spider_opened
from scrapy.spiders import Spider
from scrapy.statscollectors import StatsCollector

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
        return obj

    def spider_opened(self, spider: Spider) -> None:
        """

        :param spider:
        :type spider: Spider
        :return:
        :rtype: None
        """
        logger.info("The middleware chrome is up.")

    def spider_closed(self, spider: Spider) -> None:
        """

        :param spider:
        :type spider: Spider
        :return:
        :rtype: None
        """
        logger.info("The middleware chrome is down.")

    @as_deferred
    async def visit_page(
        self,
        request: Request,
        response: Response,
        spider: Spider,
        signal: object,
        sender: Crawler,
        *args,
        **kwargs,
    ):
        """

        :param request:
        :type request: Request
        :param response:
        :type response: Response
        :param spider:
        :type spider: Spider
        :param signal:
        :type signal: object
        :param sender:
        :type sender: Crawler
        :return:
        :rtype:
        """
        self.stats.inc_value("chrome/visit_pages")
