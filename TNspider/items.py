# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BNUItem(scrapy.Item):
    title = scrapy.Field()
    university = scrapy.Field()
    city = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    addr = scrapy.Field()
    company = scrapy.Field()
    click_times = scrapy.Field()
    fields = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()


