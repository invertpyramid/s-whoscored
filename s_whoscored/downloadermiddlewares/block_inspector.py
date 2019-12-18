"""
A middleware for block inspection by response
"""
from __future__ import annotations

import logging
from pprint import pformat
from typing import Dict, List, Union

from scrapy.http.cookies import CookieJar
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.selector.unified import Selector
from scrapy.settings import Settings
from scrapy.signals import spider_closed, spider_opened
from scrapy.spiders import Spider
from scrapy_cookies.signals import get_cookiejar

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

    def _extract_cookie_repr(
        self, response: Response, request: Request, spider: Spider
    ) -> List[Dict[str, str]]:
        """

        :param response:
        :type response: Response
        :param request:
        :type request: Request
        :param spider:
        :type spider: Spider
        :return:
        :rtype: List[Dict[str, str]]
        """
        cookiejar: CookieJar = self.crawler.signals.send_catch_log(
            get_cookiejar, response=response, request=request, spider=spider
        )[0][1]
        repr_cookiejar: List[Dict[str, str]] = []
        for x in cookiejar.make_cookies(response, request):
            repr_cookiejar.append({})
            for attr in filter(lambda y: not y.startswith("_"), dir(x)):
                if not callable(getattr(x, attr)):
                    repr_cookiejar[-1][attr] = getattr(x, attr)

        return repr_cookiejar

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

        logger.info("Response is blocked: %s", response.url)
        self.crawler.stats.inc_value("whoscored/response_blocked")

        logger.info(
            "The following cookie is invalidated:\n%s",
            pformat(self._extract_cookie_repr(response, request, spider)),
        )

        # TODO: fix the block

        return response
