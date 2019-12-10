"""
The downloadermiddlewares module developed only for this spider
"""
import functools
from asyncio.events import get_event_loop
from asyncio.futures import Future
from asyncio.tasks import ensure_future
from typing import Callable

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
