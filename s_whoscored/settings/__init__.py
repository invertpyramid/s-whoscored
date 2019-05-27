"""
The basic settings for this spider
"""
BOT_NAME = "s_whoscored"

SPIDER_MODULES = ["s_whoscored.spiders"]
NEWSPIDER_MODULE = "s_whoscored.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

SPIDER_MIDDLEWARES = {}

DOWNLOADER_MIDDLEWARES = {}

EXTENSIONS = {}

ITEM_PIPELINES = {}
