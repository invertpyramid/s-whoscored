"""
Exceptions used in this spider
"""


class WhoScoredException(Exception):
    """
    The root exception used in this spider
    """


class WhoScoredSettingsMissingException(WhoScoredException):
    """
    The necessary settings of WhoScored is missing
    """

class WhoScoredResponseBlockedException(WhoScoredException):
    """
    The response is blocked by WhoScored
    """
