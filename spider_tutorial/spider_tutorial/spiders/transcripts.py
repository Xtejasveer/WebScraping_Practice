import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies"]

    custom_settings = {
        'ROBOTSTXT_OBEY' : False,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_cloudflare_middleware.middlewares.CloudFlareMiddleware': 560
        }
    }


    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='scripts-list']/li/a")), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        print(response.url)
