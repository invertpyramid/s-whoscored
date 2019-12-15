"""
The test case for BlockInspectorMiddleware
"""

from unittest.case import TestCase
from unittest.mock import MagicMock, patch

from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse, Request
from scrapy.spiders import Spider
from scrapy.utils.test import get_crawler

from s_whoscored.downloadermiddlewares.block_inspector import BlockInspectorMiddleware
from s_whoscored.signals import response_blocked
from tests import RESPONSE_FAILED, RESPONSE_SUCCEED


class BlockInspectorMiddlewareTest(TestCase):
    """
    The test case for block inspector middleware
    """

    def setUp(self) -> None:
        self.crawler = get_crawler(Spider)
        self.spider = Spider("foo")
        self.mw = BlockInspectorMiddleware.from_crawler(self.crawler)

    def tearDown(self) -> None:
        del self.mw
        del self.spider
        del self.crawler

    def test__validate_response(self):
        with RESPONSE_FAILED.open(mode="rb") as file:
            resp = HtmlResponse(url="https://www.whoscored.com/", body=file.read())
        self.assertFalse(self.mw._validate_response(resp))
        with RESPONSE_SUCCEED.open(mode="rb") as file:
            resp = HtmlResponse(url="https://www.whoscored.com/", body=file.read())
        self.assertTrue(self.mw._validate_response(resp))

    def test_process_response(self):
        """
        Test the method of process_response
        :return:
        """
        req = Request("https://www.whoscored.com/")
        resp = HtmlResponse("https://www.whoscored.com/")

        with patch.object(self.mw, "_validate_response", new=lambda x: True):
            self.assertIs(resp, self.mw.process_response(resp, req, self.spider))

        with patch.object(self.mw, "_validate_response", new=lambda x: False):
            self.crawler.stats.inc_value = MagicMock()
            self.crawler.signals.send_catch_log = MagicMock()

            with self.assertRaises(IgnoreRequest):
                self.mw.process_response(resp, req, self.spider)

            self.crawler.stats.inc_value.assert_called_once_with(
                "whoscored/response_blocked"
            )
            self.crawler.signals.send_catch_log.assert_called_once_with(
                response_blocked, request=req, response=resp, spider=self.spider
            )
