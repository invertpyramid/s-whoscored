"""
The customized cookies downloader middleware
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Union

from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from pyppeteer.network_manager import Response as PyppeteerResponse
from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.spiders import Spider
from scrapy_cookies.downloadermiddlewares.cookies import CookiesMiddleware as CM_Origin
from websockets.client import logger as WS_C_Logger
from websockets.protocol import logger as WS_P_Logger

from s_whoscored.crawler import Crawler
from s_whoscored.downloadermiddlewares import as_deferred

logger = logging.getLogger(__name__)


class CookiesMiddleware(CM_Origin):
    """
    The customized cookies downloader middleware
    """

    def __init__(self, settings: Settings):
        """

        :param settings:
        :type settings: Settings
        """
        super(CookiesMiddleware, self).__init__(settings)
        self.browser: Optional[Browser] = None
        self.crawler: Optional[Crawler] = None

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> CookiesMiddleware:
        """

        :param crawler:
        :type crawler: Crawler
        :return:
        :rtype: CookiesMiddleware
        """
        obj: CookiesMiddleware = super(CookiesMiddleware, cls).from_crawler(crawler)
        obj.crawler = crawler

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
        super(CookiesMiddleware, self).spider_opened(spider)
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
        super(CookiesMiddleware, self).spider_closed(spider)
        await self.browser.close()

    def _convert_cookies(self, url: str, cookie: bytes) -> List[Dict[str, str]]:
        """

        :param url:
        :type url: str
        :param cookie:
        :type cookie: bytes
        :return:
        :rtype: List[Dict, [str, str]]
        """
        cookie_: List[Dict[str, str]] = []
        for item in str(cookie, encoding="ascii").split("; "):
            key, value = item.split("=", 1)
            cookie_.append({"name": key, "value": value, "url": url})
        return cookie_

    def _convert_response(
        self, response: PyppeteerResponse, container_response: Dict[str, Any]
    ) -> None:
        """

        :param response:
        :type response: PyppeteerResponse
        :param container_response:
        :type container_response: Dict[str, Any]
        :return:
        :rtype: None
        """
        container_response.update(
            {"status": response.status, "headers": response.headers}
        )

    def _validate_response(self, response: Response) -> bool:
        """

        :param response:
        :type response: Response
        :return:
        :rtype: bool
        """
        names_in_meta: List[str] = response.xpath("/html/head/meta").xpath(
            "@name"
        ).extract()

        return "ROBOTS" not in names_in_meta

    def process_response(
        self, request: Request, response: Response, spider: Spider
    ) -> Union[Response, Request]:
        """

        :param request:
        :type request: Request
        :param response:
        :type response: Response
        :param spider:
        :type spider: Spider
        :return:
        :rtype: Union[Response, Request]
        """
        # TODO: check the response blocked or not;
        #  call chrome extension to manually pass the blocking get the validated
        #  response and cookies from chrome extension
        return super(CookiesMiddleware, self).process_response(
            request, response, spider
        )
