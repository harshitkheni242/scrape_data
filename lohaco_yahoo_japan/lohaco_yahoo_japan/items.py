# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LohacoYahooJapanItem(scrapy.Item):
    # define the fields for your item here like:
    main_category_urls = scrapy.Field()
    product_link = scrapy.Field()
    product_brand = scrapy.Field()
    product_name = scrapy.Field()
    product_size = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    price_currency = scrapy.Field()
    product_stock = scrapy.Field()
    product_first_image = scrapy.Field()
    product_second_image = scrapy.Field()
    product_rating = scrapy.Field()
    product_id = scrapy.Field()


    pass
