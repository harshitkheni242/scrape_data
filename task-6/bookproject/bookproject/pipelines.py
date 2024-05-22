# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

# class BookprojectPipeline:
#     collection_name = 'product_details'
#
#     def __init__(self):
#         self.mongo_uri = "mongodb://localhost:27017/"
#         self.mongo_db = "BooksToScrape"
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri = crawler.settings.get("MONGO_URI"),
#             mongo_db = crawler.settings.get("MONGO_DATABASE", "items"),
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#
#     def close_spider(self, spider):
#         self.client.close()
#
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
#         return item



import pymongo
from scrapy.exceptions import NotConfigured
from scrapy.utils.project import get_project_settings

class BookprojectPipeline:
    collection_name = 'product_details'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MONGO_ENABLED'):
            raise NotConfigured("MongoDB is not enabled")
        mongo_uri = crawler.settings.get("MONGO_URI")
        mongo_db = crawler.settings.get("MONGO_DATABASE", "BooksToScrape")
        return cls(mongo_uri, mongo_db)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

