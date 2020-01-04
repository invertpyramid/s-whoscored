from __future__ import annotations

import logging

from scrapy.crawler import Crawler
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.settings import Settings
from scrapy.signals import spider_closed, spider_opened
from scrapy.spiders import Spider

from s_whoscored.downloadermiddlewares import as_deferred
from s_whoscored.signals import response_blocked

logger = logging.getLogger(__name__)


class Pyppeteer:
    def __init__(self, crawler: Crawler, settings: Settings):
        """

        :param crawler:
        :type crawler: Crawler
        :param settings:
        :type settings: Settings
        """
        self.crawler = crawler
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Pyppeteer:
        """

        :param crawler:
        :type crawler: Crawler
        :return:
        :rtype: Pyppeteer
        """
        obj = cls(crawler, crawler.settings)
        crawler.signals.connect(obj.spider_opened, spider_opened)
        crawler.signals.connect(obj.spider_closed, spider_closed)
        crawler.signals.connect(obj.fix_blocked_response, response_blocked)
        return obj

    def spider_opened(self, spider: Spider) -> None:
        """

        :param spider:
        :type spider: Spider
        :return:
        :rtype: None
        """
        pass

    def spider_closed(self, spider: Spider) -> None:
        """

        :param spider:
        :type spider: Spider
        :return:
        :rtype: None
        """
        pass

    @as_deferred
    async def fix_blocked_response(
        self, request: Request, response: Response, spider: Spider, *args, **kwargs
    ) -> Response:
        """

        :param request:
        :type request: Request
        :param response:
        :type response: Response
        :param spider:
        :type spider: Spider
        :return:
        :rtype: Response
        """
        return response
