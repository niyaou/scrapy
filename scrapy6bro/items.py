# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field  

class Scrapy6BroItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = Field() 
    source  = Field()
    md5     = Field()
    contentid = Field()

