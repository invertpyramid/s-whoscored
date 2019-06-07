import pprint
import re

from py_mini_racer.py_mini_racer import MiniRacer
from scrapy.http import Response
from scrapy.spiders import Spider

pp = pprint.PrettyPrinter(indent=4, width=120)

p_tournaments = re.compile(
    r"var\sallRegions\s=\s(?P<tournaments>.+?);", flags=re.DOTALL
)


class WhoScoredStatisticsSpider(Spider):
    name = "WhoScored Statistic"
    start_urls = ["https://www.whoscored.com/Statistics"]

    def parse(self, response: Response):
        """
        Parse whoscored statistic page to get all tournaments url, e.g. Premier
        League (England) as default
        :param response:
        :return:

        @url https://www.whoscored.com/Statistics
        @returns requests 1
        """
        js_script = response.css("#layout-wrapper > script::text").extract_first()
        tournaments = p_tournaments.search(js_script).group("tournaments")
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
        @returns requests 1
        """
        pass
