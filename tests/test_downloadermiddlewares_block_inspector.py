"""
TestCase for BlockInspectorMiddleware
"""

from unittest import TestCase


class BlockInspectorMiddleware(TestCase):
    """
    TODO: since pytest-twisted does not support asyncio reactor until 1.10, this
     test case will wait until the follow PR published maybe in the next
     version: https://github.com/pytest-dev/pytest-twisted/pull/63
    """

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_process_response(self):
        pass
