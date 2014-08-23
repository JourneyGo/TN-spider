# -*- coding: utf-8 -*-
import scrapy
import string
import time
# import simplejson 
import json
import calendar
# from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request

from TNspider.items import BNUItem

class TsucrawlSpider(scrapy.Spider):
    name = "TSUcrawl"
    allowed_domains = ["tsinghua.edu.cn"]
    start_urls = (
        'http://career.tsinghua.edu.cn/publish/career/8227/index.html#',
    )
    def __init__(self):
        scrapy.Spider.__init__(self)
        # self.br = webdriver.Chrome()
        
    def __del__(self):
        # self.br.quit()
        scrapy.Spider.__del__(self)
        
    def parse(self, response):
            # ajaxRq="http://career.cic.tsinghua.edu.cn/xsglxt/b/jyxt/anony/queryTodayHdList?rq=2014-05-15&callback=jsonp1408781596000"
            # yield  Request(url=ajaxRq,meta={'date': "2014-05-15"},callback=self.parse_item)
        years = [2014]
        for y in years:
            for m in range(1,13):
                dayboundary=calendar.monthrange(y,m)[1]#get day numbers in exact month
                for d in range(1,dayboundary+1):
                    ajaxRq="http://career.cic.tsinghua.edu.cn/xsglxt/b/jyxt/anony/queryTodayHdList?rq=%d-%02d-%02d&callback=jsonp14087815960%02d" % (y,m,d,d)
                    yield  Request(url=ajaxRq,meta={'date': "%d-%02d-%02d" % (y,m,d)},callback=self.parse_item)
                    
            
        
    def parse_item(self,response):
        print response.body
        result=response.body.split('(')
        result=result[1].split(')')[0]
        print result
        json2dict = eval('('+result+')')
        if json2dict:
            for dictt in json2dict:
                print dictt
                item = BNUItem()
                item['date'] = response.meta['date']
                item['university'] = 'Tsinghua'
                item['city'] = 'Beijing'
                item['title'] = dictt['bt']
                item['time'] = dictt['kssj'],dictt['jssj']
                item['addr'] = dictt['cdmcqc']
                item['link'] = "http://career.cic.tsinghua.edu.cn/xsglxt/f/jyxt/anony/gotoZpxxList?id="+dictt['zphid']
                yield Request(url=item['link'],meta={'item': item},callback=self.parse_info_item)
        else:
            print "Empty"
            return
        

    def parse_info_item(self,response):
        item = response.meta['item']
        sel_detail = Selector(response)
        desc = sel_detail.xpath('//li[@class="clearfix"]/p/a/text()').extract()
        item['desc'] = [d.encode('UTF-8') for d in desc]
        item['click_times'] = '0'
        print "Done!"
        yield item
