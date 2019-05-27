"""
the pipelines used in this project
"""
from scrapy.item import Item
from scrapy.spiders import Spider


class WhoScoredPipeline:
    """
    the pipeline used in this project
    """

    def process_item(self, item: Item, spider: Spider) -> Item:
        """

        :param item:
        :type item: Item
        :param spider:
        :type spider: Spider
        :return:
        :rtype: Item
        """
        return item
