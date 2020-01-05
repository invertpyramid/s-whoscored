from __future__ import annotations

import logging
from typing import Optional

from pyppeteer.browser import Browser, BrowserContext
from pyppeteer.launcher import launch
from pyppeteer.page import Page
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

        self.browser: Optional[Browser] = None

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

    @as_deferred
    async def spider_opened(
        self, spider: Spider, signal: object, sender: Crawler
    ) -> None:
        """

        :param spider:
        :type spider: Spider
        :param signal:
        :type signal: object
        :param sender:
        :type sender: Crawler
        :return:
        :rtype: None
        """
        self.browser = await launch(headless=False)

    @as_deferred
    async def spider_closed(
        self, spider: Spider, signal: object, sender: Crawler, reason: str
    ) -> None:
        """

        :param spider:
        :type spider: Spider
        :param signal:
        :type signal: object
        :param sender:
        :type sender: Crawler
        :param reason:
        :type reason: str
        :return:
        :rtype: None
        """
        await self.browser.close()

    @as_deferred
    async def fix_blocked_response(
        self,
        request: Request,
        response: Response,
        spider: Spider,
        signal: object,
        sender: Crawler,
    ) -> Response:
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
        :rtype: Response
        """
        context: BrowserContext = await self.browser.createIncognitoBrowserContext()
        page: Page = await context.newPage()

        # TODO: fix blocked response
        await page.goto(response.url)

        await page.close()
        await context.close()

        return response
