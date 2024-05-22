ITEM_PIPELINES = {
    'your_project_name.pipelines.MongoDBPipeline': 300,
}













import scrapy
from scrapy import Request
import pymongo

class LohacoSpider(scrapy.Spider):
    name = "lohaco"

    start_urls = [f"https://lohaco.yahoo.co.jp/sitemap_product_{i}.xml" for i in range(1, 6)]

    def parse(self, response):
        product_links = response.xpath('//loc/text()').extract()
        for link in product_links:
            yield Request(url=link, callback=self.parse_product)

    def parse_product(self, response):
        product_details = {}
        # Extract product details from response using XPath or CSS selectors
        # Populate product_details dictionary with extracted data
        yield product_details


