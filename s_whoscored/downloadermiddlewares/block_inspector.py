"""
A middleware for block inspection by response
"""
from __future__ import annotations

import logging
from typing import List, Union

from scrapy.http import Request, Response
from scrapy.selector.unified import Selector
from scrapy.settings import Settings
from scrapy.signals import spider_closed, spider_opened
from scrapy.spiders import Spider

from s_whoscored.crawler import Crawler
from s_whoscored.downloadermiddlewares import as_deferred

logger = logging.getLogger(__name__)


class BlockInspectorMiddleware:
    """
    Block inspection by response
    """

    def __init__(self, crawler: Crawler):
        """

        :param crawler:
        :type crawler: Crawler
        """
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

    @as_deferred
    async def spider_opened(self, spider: Spider, *args, **kwargs) -> None:
        """
        :param spider:
        :type spider: Spider
        :return:
        :rtype: None
        """
        logger.info("The middleware block inspector is up.")

    @as_deferred
    async def spider_closed(self, spider: Spider, *args, **kwargs) -> None:
        """
        :param spider:
        :type spider: Spider
        :return:
        :rtype: None
        """
        logger.info("The middleware block inspector is down.")

    def _validate_response(self, response: Union[Response, str]) -> bool:
        """

        :param response:
        :type response: Response
        :return:
        :rtype: bool
        """
        if isinstance(response, str):
            response: Selector = Selector(text=response)

        response: Union[Response, Selector]
        names_in_meta: List[str] = response.xpath("/html/head/meta").xpath(
            "@name"
        ).extract()

        return "ROBOTS" not in names_in_meta

    def process_response(  # pylint: disable=bad-continuation
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
        if self._validate_response(response):
            return response

        self.crawler.stats.inc_value("whoscored/response_blocked")

        # TODO: fix the block

        return response
