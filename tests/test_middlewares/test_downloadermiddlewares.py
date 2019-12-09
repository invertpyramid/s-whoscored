"""
Test cases for downloadermiddlewares modules
"""
import asyncio
from asyncio import Future
from unittest import TestCase

from scrapy.http import HtmlResponse
from twisted.internet.defer import Deferred

from s_whoscored.downloadermiddlewares import as_deferred, as_future, validate_response
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

    def test_validate_response(self):
        """
        Test the function of validate_response
        :return:
        """
        loop = asyncio.get_event_loop()

        async def test_validate_response():
            s_response_failed = await validate_response(self.s_response_failed)
            self.assertFalse(s_response_failed)
            s_response_succeed = await validate_response(self.s_response_succeed)
            self.assertTrue(s_response_succeed)

        loop.run_until_complete(test_validate_response())
        loop.close()
