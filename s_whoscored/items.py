"""
The parsers used in ItemLoader and Item's processors
"""

from scrapy.item import Item


class WhoScoredItem(Item):
    """
    The item which store all data extracted from web pages
    """
