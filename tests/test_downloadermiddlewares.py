from asyncio import Future
from unittest import TestCase

import pytest
from scrapy.http import HtmlResponse as SHtmlResponse
from twisted.internet.defer import Deferred, inlineCallbacks

from s_whoscored.downloadermiddlewares import as_deferred, as_future, validate_response
from tests import RESPONSE_FAILED, RESPONSE_SUCCEED


class DownloaderMiddlewaresTest(TestCase):
    def setUp(self) -> None:
        with RESPONSE_FAILED.open("rb") as f:
            self.s_response_failed = SHtmlResponse(url="", body=f.read())
        with RESPONSE_SUCCEED.open("rb") as f:
            self.s_response_succeed = SHtmlResponse(url="", body=f.read())

    @pytest.mark.asyncio
    async def test_validate_response_body(self):
        self.assertFalse(await validate_response(self.s_response_failed))
        self.assertTrue(await validate_response(self.s_response_succeed))

    def test_as_deferred(self):
        async def func():
            pass

        decorated_func = as_deferred(func)
        self.assertIsInstance(decorated_func(), Deferred)

    def test_as_future(self):
        d = Deferred()
        decorated_d = as_future(d)
        self.assertIsInstance(decorated_d, Future)
