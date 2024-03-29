# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
 
import scrapy


class Product(scrapy.Item):
    item_type = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    comment_count = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    commentTag = scrapy.Field()
    attribute = scrapy.Field()


class Comment(scrapy.Item):
    item_type = scrapy.Field()
    content = scrapy.Field()
    product_id = scrapy.Field()
    comment_id = scrapy.Field()
    referenceName = scrapy.Field()
    creationTime = scrapy.Field()
    attribute = scrapy.Field()


class Lost(scrapy.Item):
    item_type = scrapy.Field()      
    content = scrapy.Field()
    url = scrapy.Field()
    page = scrapy.Field()
    product_id = scrapy.Field()
    valid = scrapy.Field()


class zol_Comment(scrapy.Item):
    item_type = scrapy.Field()
    good = scrapy.Field()
    bad = scrapy.Field()
    summary = scrapy.Field()
    user = scrapy.Field()
    date = scrapy.Field()
    helpless = scrapy.Field()
    helpful = scrapy.Field()
    product_id = scrapy.Field()


class Url(scrapy.Item):
    item_type = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    platform = scrapy.Field()
    url = scrapy.Field()



