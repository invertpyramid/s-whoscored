"""
The customized cookies downloader middleware
"""
from __future__ import annotations

import gzip
import logging
from copy import copy
from typing import Any, Dict, List, Optional, Union

from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from pyppeteer.network_manager import Response as PyppeteerResponse
from pyppeteer.page import Page
from scrapy.exceptions import NotSupported
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
    async def spider_opened(  # pylint: disable=arguments-differ, bad-continuation, unused-argument
        self, spider: Spider, *args, **kwargs
    ) -> None:
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
    async def spider_closed(  # pylint: disable=arguments-differ, bad-continuation, unused-argument
        self, spider: Spider, *args, **kwargs
    ) -> None:
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

    async def _process_pyppeteer_response(  # pylint: disable=bad-continuation
        self, response: PyppeteerResponse, response_kwargs: Dict[str, Any]
    ) -> None:
        """

        :param response:
        :type response: PyppeteerResponse
        :param response_kwargs:
        :type response_kwargs: Dict[str, Any]
        :return:
        :rtype: None
        """
        if response.url == response_kwargs["url"]:
            body: str = await response.text()
            encoding: str = "utf-8"
            response_kwargs.update(
                {
                    "status": response.status,
                    "headers": response.headers,
                    "body": gzip.compress(body.encode(encoding)),
                }
            )

    def _validate_response(self, response: Response) -> bool:
        """

        :param response:
        :type response: Response
        :return:
        :rtype: bool
        """
        try:
            names_in_meta: List[str] = response.xpath("/html/head/meta").xpath(
                "@name"
            ).extract()

            return "ROBOTS" not in names_in_meta
        except NotSupported:
            return False

    @as_deferred
    async def process_response(  # pylint: disable=bad-continuation
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
        if self._validate_response(response):
            return response

        self.crawler.stats.inc_value("whoscored/blocked")

        # save the cookie into the backend
        super(CookiesMiddleware, self).process_response(request, response, spider)

        # read the cookie from the backend
        req: Request = copy(request)
        self.process_request(req, spider)
        cookie: bytes = req.headers["cookie"]

        # TODO: call chrome extension to manually pass the blocking, get the validated
        #  response and cookies from chrome extension

        response_kwargs = {
            "url": request.url,
            "flags": copy(request.flags) if request.flags else None,
            "request": request,
        }

        page: Page = await self.browser.newPage()
        page.on(
            "response", lambda x: self._process_pyppeteer_response(x, response_kwargs)
        )
        await page.setCookie(*self._convert_cookies(request.url, cookie))

        await page.goto(request.url)
        await page.waitForSelector(request.meta["waitForSelector"])

        resp = Response(**response_kwargs)

        return resp
