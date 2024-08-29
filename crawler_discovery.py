import scrapy
import json
from scrapy.crawler import CrawlerProcess


class DiscoverySpider(scrapy.Spider):
    name = 'discovery'

    results = []

    vexio_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
    }
    altex_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
    }
    qm_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
    }

    links = {
        "altex": "https://altex.ro/telefoane/cpl/filtru/p/1/",
        "vexio": "https://www.vexio.ro/smartphone/",
        "quickmobile": "https://www.quickmobile.ro/telefoane-mobile/p0"
    }
    def start_requests(self):
        for url in self.links.values():
            if "vexio.ro" in url:
                yield scrapy.Request(url, headers=self.vexio_headers,
                                     callback=self.parse_vexio)
            elif "altex.ro" in url:
                yield scrapy.Request(url, headers=self.altex_headers,
                                     callback=self.parse_altex)
            elif "quickmobile.ro" in url:
                yield scrapy.Request(url, headers=self.qm_headers,
                                     callback=self.parse_qm)
    def parse_vexio(self, response):

        phones = response.xpath(
            "//*[contains(@id,'product_box_')]"
        )
        for phone in phones:
            url = phone.xpath(".//@href").get()
            name = phone.xpath(".//*[has-class('name')]//a/text()").get()
            try:
                name = name.split("Smartphone Telefon mobil ")[1]
            except IndexError:
                name = name.split("Smartphone")[1]
            self.results.append((name, url))

        next_page_url = response.xpath(
            "//*[has-class('next-page')]//@href"
        ).extract_first()
        if next_page_url:
            yield scrapy.Request(
                next_page_url,
                callback=self.parse_vexio,
                headers=self.vexio_headers)

    def parse_altex(self, response):
        script = response.xpath(
            "//*[@id='__NEXT_DATA__']//text()"
        ).extract_first()

        data = json.loads(script)
        products = data["props"]["initialReduxState"]["catalog"][
            "currentCategory"]["products"]
        for product in products:
            name = product["name"]
            sku = product["sku"]
            url = "https://altex.ro/" + product["url_key"] + f"/cpd/{sku}/"
            elem = (name, url)
            self.results.append(elem)
        if products:
            page = response.meta.get("page", 1)
            next_page_url = response.url.replace(f"/p/{page}", f"/p/{page + 1}")
            yield scrapy.Request(next_page_url, headers=self.altex_headers,
                                 callback=self.parse_altex,
                                 meta={
                                     "page": page + 1
                                 })

    def parse_qm(self, response):
        phones = response.xpath("//*[has-class('card card-product')]")
        for phone in phones:
            url = phone.xpath(
                ".//*[has-class('card-img-product-container')]/@href"
            ).extract()[0]
            url = response.urljoin(url)
            data = phone.xpath(".//@data-product").extract_first()
            data_elm = json.loads(data)
            name = data_elm["item_brand"].capitalize() + " " + data_elm[
                "item_name"]
            self.results.append((name, url))
        #
        if phones:
            current_page = int(response.url.split("/p")[-1])
            next_page = str(current_page + 48)
            next_page_url = response.url.split("/p")[0] + "/p" + next_page
            yield scrapy.Request(
                next_page_url,
                headers=self.qm_headers)

def discovery():
    process = CrawlerProcess(settings={
            'LOG_ENABLED': False,
            # 'LOG_LEVEL': 'INFO',
        })

    # Pass the spider class to process.crawl()
    process.crawl(DiscoverySpider)

    # Start the crawling process
    process.start()

    # Retrieve the results from the spider
    res = DiscoverySpider.results
    return res
