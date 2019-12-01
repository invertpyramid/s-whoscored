"""
The basic settings for this spider
"""
import os
from typing import Any, Dict, List

from s_whoscored.exceptions import WhoScoredSettingsMissingException


def get_env(var: str, default: Any = None) -> Any:
    """
    Get the given variable's value from the environment
    :param var:
    :type var: str
    :param default:
    :type default: Any
    :return:
    :rtype: Any
    """
    try:
        return os.environ[var]
    except KeyError as exc:
        if default is None:
            raise WhoScoredSettingsMissingException from exc
        return default


BOT_NAME: str = "s_whoscored"

SPIDER_MODULES: List[str] = ["s_whoscored.spiders"]
NEWSPIDER_MODULE: str = "s_whoscored.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY: bool = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED: bool = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS: Dict[str, str] = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "en",
# }

SPIDER_MIDDLEWARES: Dict[str, int] = {}

DOWNLOADER_MIDDLEWARES: Dict[str, int] = {}

EXTENSIONS: Dict[str, int] = {}

ITEM_PIPELINES: Dict[str, int] = {}
