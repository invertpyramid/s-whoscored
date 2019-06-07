"""
The spider scrapes WhoScored Statistics page
"""
import re
from typing import Generator

from py_mini_racer.py_mini_racer import MiniRacer
from scrapy.http import Request, Response
from scrapy.spiders import Spider

P_TOUR = re.compile(r"var\sallRegions\s=\s(?P<tournaments>.+?);", flags=re.DOTALL)


class WhoScoredStatisticsSpider(Spider):
    """
    A spider inheriting the generic spider of Scrapy and scraping WhoScored
    Statistics page
    """

    name = "WhoScored Statistic"
    start_urls = ["https://www.whoscored.com/Statistics"]

    def parse(self, response: Response) -> Generator[Request, None, None]:
        """
        Parse whoscored statistic page to get all tournaments url
        :param response:
        :return:

        # Scrapy check - because of settings missing, use Premier League
        # (England) only for test purpose
        @url https://www.whoscored.com/Statistics
        @returns requests 1
        """
        js_script = response.css("#layout-wrapper > script::text").extract_first()
        tournaments = P_TOUR.search(js_script).group("tournaments")

        ctx = MiniRacer()
        for region in ctx.eval(tournaments):
            for tournament in filter(lambda x: x["name"], region["tournaments"]):
                if (region["id"], tournament["id"]) in self.settings.get(
                        "REGIONS", {(252, 2)}  # England, Premier League (as default)
                ):
                    yield response.follow(
                        tournament["url"], callback=self.parse_tournaments
                    )

    def parse_tournaments(self, response: Response):
        """

        :param response:
        :return:

        @url https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League
        @returns requests 0
        """
