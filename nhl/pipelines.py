# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import ssl

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from datetime import datetime

class MongoDBPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_collection, nhl_season):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.nhl_season = nhl_season
        self.item_list = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = "%s:%s" %(crawler.settings.get('MONGODB_SERVER'), crawler.settings.get('MONGODB_PORT')),
            mongo_db = crawler.settings.get('MONGODB_DB', 'itens'),
            mongo_collection = crawler.settings.get('MONGODB_COLLECTION'),
            nhl_season = crawler.settings.get('NHL_STANDINGS_SEASON'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        parent_list = []
        data = {
            "teams" : self.item_list,
            "weekday" : datetime.now().weekday(),
            "season" : self.nhl_season,
            "created_date": datetime.now()
        }
        parent_list.append(data)

        self.db[self.mongo_collection].insert(parent_list)
        self.client.close()

    def process_item(self, item, spider):
        self.item_list.append(item);
        return item
