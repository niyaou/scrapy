# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json  
import codecs  
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class Scrapy6BroPipeline(object):



    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):

        return cls(
            mongo_uri = "mongodb://localhost:27017",
            mongo_db ="src6bro"
        )

    def open_spider(self, spider):                  #爬虫一旦开启，就会实现这个方法，连接到数据库
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):            #爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        self.client.close()

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + '\n'  
        # # print line  
        # self.file.write(line.encode('latin-1').decode('unicode_escape'))  

        # return item  

        valid = True
        table = self.db['budejie']
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
           

        # if valid:
        #     # line = json.dumps(dict(item)).encode('latin-1').decode('unicode_escape')
        if  table.find_one({"md5":item['md5']}) :
            pass
        else :
            line = dict(item)
            table.insert_one(dict(line))
            
            
        # table.update({"md5":item['md5']},{"$set":dict(line)})
 
        return item
     
