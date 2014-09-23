# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import string
import codecs
import MySQLdb
import MySQLdb.cursors
from scrapy import log
from TNspider.items import BNUItem
from twisted.enterprise import adbapi

class MysqlPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                    # host = '127.0.0.1',
                    # db = 'jobinfo',#
                    user = 'root',
                    # passwd = 'root',
                    cursorclass = MySQLdb.cursors.DictCursor,
                    charset = 'utf8',
                    use_unicode = True
                    )
                    
    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self.handle_error)
#        print item
        return item
        
    def _conditional_insert(self,tx,item):
        if item.get('title'):
            tx.execute(\
                "insert into jobinfo (title,university,time,address,link,date,click_times,flag,abbreviation,description,city)\
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                "".join(item['title']),
                "".join(item['university']),
                "".join(item['time']),
                "".join(item['addr']),
                item['link'],
                "".join(item['date']),
                string.atoi("".join(item['click_times']),),
                item['flag'],
                item['abbreviation'],
                ''.join(item['desc']),
                ''.join(item['city'])
                )
                )
    def handle_error(self,e):
        log.err(e)
