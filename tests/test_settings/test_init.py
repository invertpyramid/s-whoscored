"""
TestCases for the functions and classes in the module of s_whoscored.settings.__init__
"""
import os
from typing import Any
from unittest.case import TestCase
from unittest.mock import patch

from s_whoscored.exceptions import WhoScoredSettingsMissingException
from s_whoscored.settings import get_env


class SettingsFunctionsTest(TestCase):
    """
    The test case for functions in settings modules
    """

    def test_get_env_var(self):
        """
        Test the function of get_env in settings modules
        :return:
        """
        with patch.dict(os.environ, {}):
            with self.assertRaises(WhoScoredSettingsMissingException):
                _: Any = get_env("NOT_EXIST")
            self.assertEqual(get_env("NOT_EXIST", default="VAL"), "VAL")
            self.assertEqual(get_env("NOT_EXIST", default=False), False)

        with patch.dict(os.environ, {"VAR": "VAL"}):
            self.assertEqual(get_env("VAR"), "VAL")
            self.assertEqual(get_env("VAR", default="OTHER_VAL"), "VAL")
            self.assertNotEqual(get_env("VAR", default="OTHER_VAL"), "OTHER_VAL")
