"""
run script for this scrapy project
"""
import sys
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

sys.path.append(str(Path("/").joinpath(*Path(__file__).parts[:-2])))

modules = [
    "s_whoscored.settings.autothrottle",
    "s_whoscored.settings.concurrent",
    "s_whoscored.settings.cookies",
    "s_whoscored.settings.httpcache",
    "s_whoscored.settings.log",
    "s_whoscored.settings.sentry",
    "s_whoscored.settings.user_agent",
    "s_whoscored.settings.whoscored",
]

if __name__ == "__main__":
    settings = get_project_settings()

    for module in modules:
        settings.setmodule(module=module)

    process = CrawlerProcess(settings=settings)

    process.crawl("WhoScored")

    process.start()
