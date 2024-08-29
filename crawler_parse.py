import scrapy
from scrapy.crawler import CrawlerProcess
import json
import re


class Parser(scrapy.Spider):
    name = 'dynamic'
    vexio_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
    }
    altex_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',

    }

    def __init__(self, urls=None, *args, **kwargs):
        super(Parser, self).__init__(*args, **kwargs)
        if urls is None:
            urls = []
        self.start_urls = urls

    def start_requests(self):
        for url in self.start_urls:
            if "vexio.ro" in url:
                yield scrapy.Request(url, headers=self.vexio_headers,
                                     callback=self.parse_vexio)
            elif "altex.ro" in url:
                yield scrapy.Request(url, headers=self.altex_headers,
                                     callback=self.parse_altex)

    def parse_vexio(self, response):

        def clean_json_string(json_string):
            json_string = re.sub(r'[\x00-\x1F\x7F]', '', json_string)
            return json_string

        # Extract data you want from the page
        script = response.xpath(
            "//*[@type='application/ld+json']//text()"
        ).extract()[-1]

        data = json.loads(clean_json_string(script))

        price = data["offers"]["price"]

        elem = {
            "url": response.url,
            "price": float(price)
        }
        yield elem

    def parse_altex(self, response):
        script = response.xpath(
            "//*[@type='application/ld+json']//text()"
        ).extract()[0]

        data = json.loads(script)
        price = data["offers"][0]["priceSpecification"]["price"]
        elem = {
            "url": response.url,
            "price": float(price)
        }
        yield elem


# if __name__ == '__main__':
#     urls_to_scrape = [
#         'https://www.vexio.ro/smartphone/apple/2396668-iphone-15-128gb-6gb-ram-5g-black/',
#         'https://www.vexio.ro/telefoane-mobile/maxcom/307579-mm720bb-single-sim-black/',
#         'https://altex.ro/telefon-samsung-galaxy-a25-5g-128gb-6gb-ram-dual-sim-blue-black/cpd/SMTSA255G6BK/'
#     ]
#
#     # Set up the CrawlerProcess with custom settings if needed
#     process = CrawlerProcess(settings={
#         'FEEDS': {
#             'data.json': {
#                 'format': 'json',
#                 'overwrite': True,
#             },
#         },
#     })
#
#     # Start the crawling process
#     process.crawl(Parser, urls=urls_to_scrape)
#     process.start()
