from scrapy.crawler import Crawler as C_Origin
from scrapy.crawler import CrawlerProcess as CP_Origin


class Crawler(C_Origin):
    def __init__(self, spidercls, settings, crawler_process):
        super(Crawler, self).__init__(spidercls, settings)
        self.crawler_process = crawler_process


class CrawlerProcess(CP_Origin):
    def _create_crawler(self, spidercls):
        if isinstance(spidercls, str):
            spidercls = self.spider_loader.load(spidercls)
        return Crawler(spidercls, self.settings, self)
