"""
Test cases for downloadermiddlewares modules
"""
import asyncio
from asyncio import Future
from unittest import TestCase

from scrapy.http import HtmlResponse
from twisted.internet.defer import Deferred

from s_whoscored.downloadermiddlewares import as_deferred, as_future
from tests import RESPONSE_FAILED, RESPONSE_SUCCEED


class DownloaderMiddlewaresTest(TestCase):
    """
    The test case for downloadermiddlewares modules
    """

    def setUp(self) -> None:
        with RESPONSE_FAILED.open("rb") as file:
            self.s_response_failed = HtmlResponse(url="", body=file.read())
        with RESPONSE_SUCCEED.open("rb") as file:
            self.s_response_succeed = HtmlResponse(url="", body=file.read())

    def test_as_deferred(self):
        """
        Test the function as_deferred, which convert Future to Deferred
        """

        async def func():
            pass

        decorated_func = as_deferred(func)
        self.assertIsInstance(decorated_func(), Deferred)

    def test_as_future(self):
        """
        Test the function as_future, which convert Deferred to Future
        """
        deferred = Deferred()
        decorated_d = as_future(deferred)
        self.assertIsInstance(decorated_d, Future)
