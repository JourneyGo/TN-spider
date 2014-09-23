# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 16:31:20 2014

@author: xzd
"""

# -*- coding: utf-8 -*-
import scrapy
import string
import time
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request

from TNspider.items import BNUItem

class BnucrawlSpider(scrapy.Spider):
    name = "BUPTcrawl"
    allowed_domains = ["bupt.edu.cn"]
    start_urls = (
        'http://job.bupt.edu.cn/home/fairs',
    )
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.br = webdriver.Chrome()
    def __del__(self):
        self.br.quit()
        scrapy.Spider.__del__(self)
        
        
    def parse(self, response):
        sel = Selector(response)
        self.br.get(response.url)
#        total_pages = "".join(sel.xpath('//div[@id="AspNetPager1"]//a[last()]/@href').extract()).split("'")[-2]
#        pagenums = string.atoi(total_pages)
        pagenums = 1
        print pagenums
        for pagenum in range(1,pagenums+1):
            sites = sel.xpath('//*[@id="main-center"]/div[1]/div[3]/ul/li')
            for site in sites:
                item = BNUItem()
                item['university'] = "北京邮电大学"
                item['city'] = "北京"
                title = site.xpath('.//span[1]/a/text()').extract()
                item['title'] = [t.encode('UTF-8') for t in title]
                link = site.xpath('.//span[1]/a/@href').extract()
                item['link'] = "".join([l.encode('UTF-8') for l in link])
                yield Request(url=item['link'], meta={'item': item},
                              callback=self.parse_item)
#            action_link = self.br.find_element_by_link_text("下一页")
#            action_link.click()
#            time.sleep(5)
#            sel = Selector(text=self.br.page_source)
        self.br.close()
            

    def parse_item(self,response):
        item = response.meta['item']
        sel_detail = Selector(response)
        desc = sel_detail.xpath('//html/body/div[2]/div/descendant::text()').extract()
        item['desc'] = [d.encode('UTF-8') for d in desc]
        date_temp = sel_detail.xpath('//html/body/div[2]/div/div[3]/div[3]/span[2]/text()').extract()
        date_time = date_temp[0]
        date = date_time[0:10]
        print date
        holdingTime = date_time[11:]
        print holdingTime
        item['date'] = [t.encode('UTF-8') for t in date]
        item['time'] = [t.encode('UTF-8') for t in holdingTime]
        yield item
