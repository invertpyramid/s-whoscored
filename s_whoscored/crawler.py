"""
Enhance Crawler

Add a property into Crawler to point CrawlerProcess, which creates Crawler
"""
from typing import Union

from scrapy.crawler import Crawler as C_Origin
from scrapy.crawler import CrawlerProcess as CP_Origin
from scrapy.spiders import Spider


class Crawler(C_Origin):
    """
    Enhanced Crawler with an extra property crawler_process
    """

    def __init__(self, spidercls, settings, crawler_process):
        super(Crawler, self).__init__(spidercls, settings)
        self.crawler_process = crawler_process


class CrawlerProcess(CP_Origin):
    """
    Pass self as an argument to the method of crawler creation
    """

    def _create_crawler(self, spidercls: Union[str, Spider]) -> Crawler:
        """

        :param spidercls:
        :type spidercls: Union[str, Spider]
        :return:
        """
        if isinstance(spidercls, str):
            spidercls = self.spider_loader.load(spidercls)
        return Crawler(spidercls, self.settings, self)
