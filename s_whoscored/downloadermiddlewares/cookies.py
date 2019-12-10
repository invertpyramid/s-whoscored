"""
The customized cookies downloader middleware
"""
from __future__ import annotations

from typing import List, Optional, Union

from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.spiders import Spider
from scrapy_cookies.downloadermiddlewares.cookies import CookiesMiddleware as CM_Origin

from s_whoscored.crawler import Crawler


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
        return obj

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
