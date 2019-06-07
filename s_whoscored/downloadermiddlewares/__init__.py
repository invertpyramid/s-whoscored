"""
The downloadermiddlewares module developed only for this spider
"""
import functools
from asyncio.events import get_event_loop
from asyncio.futures import Future
from asyncio.tasks import ensure_future
from typing import Callable, List, Union

from pyppeteer.page import Page
from scrapy.http import HtmlResponse, Response
from twisted.internet.defer import Deferred


def as_deferred(func) -> Callable[..., Deferred]:
    """
    Convert Future to Deferred
    :param func:
    :type func: Callable
    :return:
    :type: Callable[..., Deferred]
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return Deferred.fromFuture(ensure_future(func(*args, **kwargs)))

    return wrapper


def as_future(deferred: Deferred) -> Future:
    """
    Convert Deferred to Future
    :param deferred:
    :type deferred: Deferred
    :return:
    :type: Future
    """
    return deferred.asFuture(get_event_loop())


async def validate_response(response: Union[Response, Page]) -> bool:
    """
    Validate the response by its content
    :param response:
    :type response: Union[Response, Page]
    :return:
    :rtype: bool
    """
    if isinstance(response, Page):
        content: str = await response.content()
        body: bytes = content.encode()
        response, _ = HtmlResponse(url="", body=body), response

    names_in_meta: List[str] = response.xpath("/html/head/meta").xpath(
        "@name"
    ).extract()

    return "ROBOTS" not in names_in_meta
