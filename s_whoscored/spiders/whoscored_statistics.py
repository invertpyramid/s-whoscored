"""
The spider scrapes WhoScored Statistics page
"""
import re
from collections import namedtuple
from typing import Generator, List

from py_mini_racer.py_mini_racer import MiniRacer
from scrapy.http import Request, Response
from scrapy.spiders import Spider

P_TOUR = re.compile(r"var\sallRegions\s=\s(?P<tournaments>.+?);", flags=re.DOTALL)
P_TEAM = re.compile(
    r"DataStore\.prime\('history', {.+?},(?P<history>\[.+?\])\);", flags=re.DOTALL
)
P_TEAM_FIXTURES = re.compile(
    r"DataStore\.prime\('teamfixtures',\s\$\.extend\(.+?\),\s(?P<fixtures>\[.+?\])\);",
    flags=re.DOTALL,
)

Team = namedtuple(
    "Team",
    [
        "season_id",
        "id",
        "name",
        "rank",
        "p0",
        "rank_home",
        "p1",
        "rank_away",
        "p2",
        "region",
        "region_id",
    ],
)

Match = namedtuple(
    "Match",
    [
        "id",
        "p0",
        "date",
        "time",
        "home_id",
        "home",
        "home_red_card",
        "away_id",
        "away",
        "away_red_card",
        "full",
        "half",
        "p3",
        "p4",
        "penalty",
        "season",
        "tournament",
        "p5",
        "tournament_id",
        "region_id",
        "season_id",
        "stage_id",
        "tournament_abbr",
        "p7",
        "p8",
        "p9",
        "p10",
        "p11",
        "home_region",
        "away_region",
        "p13",
    ],
)


class WhoScoredStatisticsSpider(Spider):
    """
    A spider inheriting the generic spider of Scrapy and scraping WhoScored
    Statistics page
    """

    name: str = "WhoScored Statistic"

    def start_requests(self) -> Generator[Request, None, None]:
        yield Request(
            url="https://www.whoscored.com/Statistics",
            callback=self.parse,
            meta={
                "cookiejar": "whoscored",
                "waitForSelector": "#layout-wrapper > script",
            },
        )

    def parse(self, response: Response) -> Generator[Request, None, None]:
        """
        Parse whoscored statistic page to get all tournaments url
        :param response:
        :type response: Response
        :return:
        :rtype: Generator[Request, None, None]

        # Scrapy check - because of settings missing, use Premier League
        # (England) only for test purpose
        @url https://www.whoscored.com/Statistics
        @returns requests 1
        """
        js_script: str = response.css("#layout-wrapper > script::text").extract_first()
        tournaments: str = P_TOUR.search(js_script).group("tournaments")

        ctx = MiniRacer()
        for region in ctx.eval(tournaments):
            for tournament in filter(lambda x: x["name"], region["tournaments"]):
                if (region["id"], tournament["id"]) in self.settings.get(
                    "REGIONS", {(252, 2)}  # pylint: disable=bad-continuation
                ):  # England, Premier League (as default)
                    yield response.follow(
                        tournament["url"],
                        callback=self.parse_tournaments,
                        meta={"waitForSelector": "#layout-content-wrapper"},
                    )

    def parse_tournaments(self, response: Response) -> Generator[Request, None, None]:
        """
        TODO: here are two methods:

         1. go to seasons, and fetch all fixtures in one season
         2. go to team statistics, and fetch all games for each of teams
        :param response:
        :type response: Response
        :return:
        :rtype: Generator[Request, None, None]

        @url https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League
        @returns requests 0
        """
        # This is to go for method 1
        # for season in response.css("#seasons option"):
        #     url = season.css("option::attr(value)").extract_first()
        #     yield response.follow(url, callback=self.parse_season)

        # This is to go for method 2
        js_script: str = response.xpath(
            '//*[@id="layout-content-wrapper"]/div[2]/script[4]'
        ).extract_first()

        ctx = MiniRacer()
        team: List
        for team in ctx.eval(P_TEAM.search(js_script).group("history")):
            team_: Team = Team(*team)
            yield response.follow(
                url="https://www.whoscored.com/Teams/{id}/Fixtures/".format(
                    id=team_.id
                ),
                callback=self.parse_team,
                meta={"waitForSelector": "layout-content-wrapper"},
            )

            break

    def parse_season(self, response: Response) -> Generator[Request, None, None]:
        """

        :param response:
        :type response: Response
        :return:
        :rtype: Generator[Response, None, None]
        """

    def parse_team(self, response: Response) -> Generator[Request, None, None]:
        """

        :param response:
        :type response: Response
        :return:
        :rtype: Generator[Request, None, None]

        @url https://www.whoscored.com/Teams/167/Fixtures/England-Manchester-City
        @returns requests 0
        """
        js_script: str = response.xpath(
            '//*[@id="layout-content-wrapper"]/div[2]/script[3]'
        ).extract_first()

        ctx = MiniRacer()

        fixture: List
        for fixture in ctx.eval(P_TEAM_FIXTURES.search(js_script).group("fixtures")):
            fixture_: Match = Match(*fixture)
            yield response.follow(
                url="https://www.whoscored.com/Matches/{id}/".format(id=fixture_.id),
                callback=self.parse_match,
            )

    def parse_match(self, response: Response) -> Generator[Request, None, None]:
        """

        :param response:
        :type response: Response
        :return:
        :rtype: Generator[Request, None, None]
        """
