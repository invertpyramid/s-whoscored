import logging

from scrapy_httpcache.downloadermiddlewares.httpcache import (
    AsyncHttpCacheMiddleware as AHM_Original,
)

from s_whoscored.downloadermiddlewares import as_future

logger = logging.getLogger(__name__)


class AsyncHttpCacheMiddleware(AHM_Original):
    """

    """

    def remove_banned(self, spider, response, exception, **kwargs):
        as_future(self.storage.remove_response(spider, response.request, response))
        self.stats.inc_value("httpcache/store", count=-1, spider=spider)
        logger.warning("Remove banned response cache: {}".format(response.request.url))
