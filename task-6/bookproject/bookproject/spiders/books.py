import csv
from typing import Iterable
from parsel import Selector
import scrapy
import parsel
from scrapy import Request
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher


class BooksSpider(scrapy.Spider):
    name = "books"

    def start_requests(self):
        URL = 'https://books.toscrape.com/'
        yield scrapy.Request(url=URL, callback=self.parse)

    def parse(self, response):
        for selector in response.xpath('//article[@class="product_pod"]'):
            if 'catalogue' in selector.xpath('.//h3/a/@href').get(''):
                domain_link = 'https://books.toscrape.com/'
            else:
                domain_link = 'https://books.toscrape.com/catalogue/'

            yield {
                'product_link': domain_link + selector.xpath('.//h3/a/@href').get(''),
                'title': selector.xpath('.//h3/a/@title').get(),
                'image': 'https://books.toscrape.com/' + selector.xpath('.//div[@class="image_container"]/a/img/@src').get(''),
                'price': selector.xpath('.//div[@class="product_price"]/p[@class="price_color"]/text()').get('')
            }

        next_page_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

def book_spider_result():
    books_results = []

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'books_data.csv',
        'MONGO_ENABLED': True,
        'MONGO_URI': 'mongodb://localhost:27017/',
        'MONGO_DATABASE': 'BooksToScrape'
    })

    process.crawl(BooksSpider)
    process.start()

if __name__ == '__main__':
    book_spider_result()
