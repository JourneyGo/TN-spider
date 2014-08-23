# -*- coding: utf-8 -*-
import scrapy
import string
import time
import simplejson 
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
        
        ajaxRq="http://career.cic.tsinghua.edu.cn/xsglxt/b/jyxt/anony/queryTodayHdList?rq=2014-04-08&callback=jsonp1408781593994"
        yield  Request(url=ajaxRq,callback=self.parse_item)
            
        
    def parse_item(self,response):
        print response
        print response.body
        result=response.body.split('[')
        result=result[1].split(']')
        print result[0]
        
        dictinfo = simplejson.loads(result[0])
        result=simplejson.dumps(dictinfo)
        print result
        
        # item = response.meta['item']
        # sel_detail = Selector(response)
        # desc = sel_detail.xpath('//div[@class="i3001 job1list empnr intorone02"]/descendant::text()').extract()
        # item['desc'] = [d.encode('UTF-8') for d in desc]
        # yield item
