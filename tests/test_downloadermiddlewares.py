import asyncio
from asyncio import Future
from unittest import TestCase

from scrapy.http import HtmlResponse as SHtmlResponse
from twisted.internet.defer import Deferred

from s_whoscored.downloadermiddlewares import as_deferred, as_future, validate_response
from tests import RESPONSE_FAILED, RESPONSE_SUCCEED


class DownloaderMiddlewaresTest(TestCase):
    def setUp(self) -> None:
        with RESPONSE_FAILED.open("rb") as f:
            self.s_response_failed = SHtmlResponse(url="", body=f.read())
        with RESPONSE_SUCCEED.open("rb") as f:
            self.s_response_succeed = SHtmlResponse(url="", body=f.read())

    def test_validate_response(self):
        loop = asyncio.get_event_loop()

        async def test_validate_response():
            s_response_failed = await validate_response(self.s_response_failed)
            self.assertFalse(s_response_failed)
            s_response_succeed = await validate_response(self.s_response_succeed)
            self.assertTrue(s_response_succeed)

        loop.run_until_complete(test_validate_response())
        loop.close()

    def test_as_deferred(self):
        async def func():
            pass

        decorated_func = as_deferred(func)
        self.assertIsInstance(decorated_func(), Deferred)

    def test_as_future(self):
        d = Deferred()
        decorated_d = as_future(d)
        self.assertIsInstance(decorated_d, Future)
