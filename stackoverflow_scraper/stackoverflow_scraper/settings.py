
BOT_NAME = "stackoverflow_scraper"

SPIDER_MODULES = ["stackoverflow_scraper.spiders"]
NEWSPIDER_MODULE = "stackoverflow_scraper.spiders"

ROBOTSTXT_OBEY = False

FEEDS = {
    'stackoverflow_data.json': {
        'format': 'json',
        'encoding': 'utf8',
        'indent': 4,
        'store_empty': False,
        'fields': None,
        'overwrite': True,
    },
}

USER_AGENT = "stackoverflow_scraper/1.0 (+http://www.yourdomain.com)"

DOWNLOAD_DELAY = 1  
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

RETRY_ENABLED = True
RETRY_TIMES = 5  
RETRY_HTTP_CODES = [418, 429, 500, 503]  

# LOG_LEVEL = "ERROR"

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
