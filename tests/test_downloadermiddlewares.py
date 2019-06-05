from unittest import TestCase

import pytest
from scrapy.http import HtmlResponse as SHtmlResponse

from s_whoscored.downloadermiddlewares import validate_response
from tests import RESPONSE_FAILED, RESPONSE_SUCCEED


class DownloaderMiddlewaresTest(TestCase):
    def setUp(self) -> None:
        with RESPONSE_FAILED.open("rb") as f:
            self.response_failed = SHtmlResponse(url="", body=f.read())
        with RESPONSE_SUCCEED.open("rb") as f:
            self.response_succeed = SHtmlResponse(url="", body=f.read())

    @pytest.mark.asyncio
    async def test_validate_response_body(self):
        self.assertFalse(await validate_response(self.response_failed))
        self.assertTrue(await validate_response(self.response_succeed))
