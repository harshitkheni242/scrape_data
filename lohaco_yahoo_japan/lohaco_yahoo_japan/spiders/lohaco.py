import json
import os
import re
import scrapy
import requests
from ..items import LohacoYahooJapanItem
from lohaco_yahoo_japan.config import extract_size
from scrapy.spiders import CrawlSpider


class LohacoSpider(scrapy.Spider):
    name = 'lohaco'

    category_list = [f"https://lohaco.yahoo.co.jp/sitemap_product_{i}.xml" for i in range(1, 6)]

    start_urls = []
    for link in start_urls:
       product_link = link


    os.chdir('../../')

    current_directory = os.getcwd()

    html_path = os.path.join(current_directory, 'lohaco_yahoo_pdp_file_save')

    try:
        if not os.path.exists(html_path):
            os.makedirs(html_path)
    except Exception as e:
        print(e)

    filename = '/site_map_category.html'
    path = html_path + filename
    path = path.replace("\\", "/")

    for c_link in category_list:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                res = f.read()
        else:
            product_link = requests.get(c_link)
            res = product_link.text
            with open(path, 'w', encoding='utf-8') as f:
                f.write(res)

        if res:
            lss = re.findall('<loc>(.*?)</loc>', res)
            for kk in lss:
                start_urls.append(kk)
        else:
            print(c_link, "wrong response")


    def parse(self, response):
        items = LohacoYahooJapanItem()

        # Define product_link as a local variable
        product_link = response.url

        product_details_json = response.xpath("//script[@type='application/ld+json']/text()").get('')
        product_details = json.loads(product_details_json)
        try:
            product_brand = product_details['brand']['name']
        except:
            product_brand = ''

        try:
            product_name = product_details['name']
        except:
            product_name = ''
            return None

        try:
            product_size = extract_size(product_name)
        except:
            product_size = ''

        try:
            description = product_details['description']
        except:
            description = ''

        try:
            price = product_details['offers']['price']
        except:
            price = ''

        try:
            price_currency = product_details['offers']['priceCurrency']
        except:
            price_currency = ''

        try:
            product_stock = response.xpath("//p[@class='font-weight-bold text-h4 text-sm-h2 ma-0']/text()").get('')
        except:
            product_stock = ''

        try:
            product_images = [image.replace("/r/", "/n/") for image in
                              response.xpath("//div[@class='thumbs']/div/img/@src").getall()]
            product_first_image = product_images[0] if product_images else ''
            product_second_images = "|".join(product_images[1:]) if len(product_images) > 1 else ''
        except:
            product_first_image = ''
            product_second_images = ''

        try:
            product_rating = product_details['aggregateRating']['ratingValue']
        except:
            product_rating = ''

        try:
            item_number = response.url.split("/")[-2]
        except:
            item_number = ''

        try:
            main_category_urls = LohacoSpider.c_link
        except:
            main_category_urls = ''

        items['main_category_urls'] = main_category_urls
        items['product_link'] = product_link
        items["product_brand"] = product_brand
        items['product_name'] = product_name
        items['product_size'] = product_size
        items['description'] = description
        items["price"] = price
        items["price_currency"] = price_currency
        items["product_stock"] = product_stock
        items["product_first_image"] = product_first_image
        items["product_second_image"] = product_second_images
        items["product_rating"] = product_rating
        items['product_id'] = item_number

        yield items
