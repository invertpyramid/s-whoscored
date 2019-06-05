"""
A middleware for block inspection
"""

from scrapy.crawler import Crawler
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.spiders import Spider

from s_whoscored.downloadermiddlewares import as_deferred, validate_response


class BlockInspectorMiddleware:
    def __init__(self, crawler: Crawler):
        self.crawler: Crawler = crawler
        self.settings: Settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        obj = cls(crawler=crawler)
        return obj

    @as_deferred
    async def process_response(
        self, response: Response, request: Request, spider: Spider
    ) -> Response:
        """

        :param request:
        :type request: Request
        :param response:
        :type response: Response
        :param spider:
        :type spider: Spider
        :return:
        :rtype:
        """
        if await validate_response(response):
            return response
        else:
            raise IgnoreRequest
