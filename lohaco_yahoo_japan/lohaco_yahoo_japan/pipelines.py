# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class LohacoYahooJapanPipeline:
    def __init__(self):
        self.mongo_db()

    def mongo_db(self):
        self.conn = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.conn['lohaco_yahoo_product']
        self.collections = self.db['products']


    def process_item(self, item, spider):
        self.collections.insert_one(dict(item))
        self.collections.create_index('product_id', unique=True)
        return item