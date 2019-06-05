"""
run script for this scrapy project
"""
import sys
from asyncio import get_event_loop
from pathlib import Path

from scrapy.utils.misc import load_object
from scrapy.utils.project import get_project_settings
from twisted.internet import asyncioreactor

sys.path.append(str(Path("/").joinpath(*Path(__file__).parts[:-2])))

asyncioreactor.install(get_event_loop())

CrawlerProcess = load_object("s_whoscored.crawler.CrawlerProcess")

modules = [
    "s_whoscored.settings.autothrottle",
    "s_whoscored.settings.block_inspector",
    "s_whoscored.settings.concurrent",
    "s_whoscored.settings.cookies",
    "s_whoscored.settings.httpcache",
    "s_whoscored.settings.httpproxy",
    "s_whoscored.settings.log",
    "s_whoscored.settings.pyppeteer",
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
