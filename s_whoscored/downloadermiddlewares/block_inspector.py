"""
A middleware for block inspection by response
"""
from __future__ import annotations

import logging
from typing import List, Optional, Union

from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from pyppeteer.page import Page
from scrapy.http import Request, Response
from scrapy.selector.unified import Selector
from scrapy.settings import Settings
from scrapy.signals import spider_closed, spider_opened
from scrapy.spiders import Spider
from websockets.client import logger as WS_C_Logger
from websockets.protocol import logger as WS_P_Logger

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

        self.browser: Optional[Browser] = None

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

        WS_C_Logger.setLevel(crawler.settings["WS_C_LOG_LEVEL"])
        WS_P_Logger.setLevel(crawler.settings["WS_P_LOG_LEVEL"])

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

        self.browser: Browser = await launch(
            headless=False, logLevel=self.settings["BROWSER_LEVEL"]
        )

    @as_deferred
    async def spider_closed(self, spider: Spider, *args, **kwargs) -> None:
        """
        :param spider:
        :type spider: Spider
        :return:
        :rtype: None
        """
        logger.info("The middleware block inspector is down.")

        await self.browser.close()

    async def _process_pyppeteer_response(  # pylint: disable=bad-continuation
        self, response: Response, request: Request, spider: Spider
    ) -> Response:
        """
        TODO: resolve the blocked response
        :param response:
        :type response: Response
        :param request:
        :type request: Request
        :param spider:
        :type spider: Spider
        :return:
        :rtype: Response
        """
        page: Page = await self.browser.newPage()
        await page.close()

        return response

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
        if self._validate_response(response):
            return response

        self.crawler.stats.inc_value("whoscored/response_blocked")

        resp: Response = await self._process_pyppeteer_response(
            response, request, spider
        )

        return resp
