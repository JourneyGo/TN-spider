# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 16:56:40 2014

@author: xzd
"""
# -*- coding: utf-8 -*-
import scrapy
#import string
import time
import calendar
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver

from TNspider.items import BNUItem

class BITcrawlSpider(scrapy.Spider):
    name = "BITcrawl"
    allowed_domains = ["bit.edu.cn"]
    start_urls = (
        'http://job.bit.edu.cn/employment-activities.html?tx_extevent_pi1%5Bdate%5D=2013-10-18',
    )
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.br = webdriver.Chrome()
        print "准备爬取 北京理工大学 宣讲会数据"
    def __del__(self):
        self.br.quit()
        scrapy.Spider.__del__(self)
        
    def parse(self, response):
        sel = Selector(response)
        home_url = "http://job.bit.edu.cn/"       
        years = [2013,2014]
        for y in years:
            for m in range(1,13):
                dayboundary=calendar.monthrange(y,m)[1]#get day numbers in exact month
                for d in range(1,dayboundary+1):
                    urlRq="http://job.bit.edu.cn/employment-activities.html?tx_extevent_pi1%5Bdate%5D="+"%d-%02d-%02d" % (y,m,d)
                    self.br.get(urlRq)
                    time.sleep(1)
                    sel = Selector(text = self.br.page_source)
                    sites = sel.xpath('//table[@id="font_event_list_table"]/tbody/tr')
                    for site in sites:
                        item = BNUItem()
                        item['university'] = "北京理工大学"
                        item['city'] = "北京"
                        clicks = site.xpath('.//td[4]/text()').extract()
                        item['click_times'] = "".join([t.encode('UTF-8') for t in clicks])
                        item['date'] = '%d-%02d-%02d'%(y,m,d)
                        print item['date']
                        # 没有使用网页显示的时间，因为网页显示的时间包括几点开始几点结束，格式不对
                        title = site.xpath('.//td[1]/a/text()').extract()
                        item['title'] = [t.encode('UTF-8') for t in title]
                        link = site.xpath('.//td[1]/a/@href').extract()
                        # print link
                        item['link'] = home_url+"".join([l.encode('UTF-8') for l in link])
                        yield Request(url=item['link'], meta={'item': item},
                                      callback=self.parse_item)
            
    def parse_item(self,response):
        sel_detail = Selector(response)
        item = response.meta['item']
        desc = sel_detail.xpath('//*[@id="event_preview"]/descendant::text()').extract()
        item['desc'] = [d.encode('UTF-8') for d in desc]
        print "Done!"
        yield item

