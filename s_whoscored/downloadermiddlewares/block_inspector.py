"""
A middleware for block inspection by response
"""
from __future__ import annotations

import logging

from scrapy.crawler import Crawler
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.signals import spider_closed, spider_opened
from scrapy.spiders import Spider

from s_whoscored.downloadermiddlewares import as_deferred, validate_response

logger = logging.getLogger(__name__)


class BlockInspectorMiddleware:
    """
    Block inspection by response
    """

    def __init__(self, crawler: Crawler):
        self.crawler: Crawler = crawler
        self.settings: Settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> BlockInspectorMiddleware:
        """
        Initial a middleware instance with crawler
        :param crawler:
        :type crawler: Crawler
        :return:
        :rtype: BlockInspectorMiddleware
        """
        obj = cls(crawler=crawler)
        crawler.signals.connect(obj.spider_opened, spider_opened)
        crawler.signals.connect(obj.spider_closed, spider_closed)
        return obj

    def spider_opened(self, spider: Spider) -> None:
        logger.info("The middleware block inspector is up.")

    def spider_closed(self, spider: Spider) -> None:
        logger.info("The middleware block inspector is down.")

    @as_deferred
    async def process_response(  # pylint: disable=bad-continuation
        self, response: Response, request: Request, spider: Spider
    ) -> Response:
        """
        Inspect block by the content of response
        :param request:
        :type request: Request
        :param response:
        :type response: Response
        :param spider:
        :type spider: Spider
        :return:
        :rtype: Response
        """
        if await validate_response(response):
            return response
        raise IgnoreRequest
