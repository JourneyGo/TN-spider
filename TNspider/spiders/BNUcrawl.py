# -*- coding: utf-8 -*-
import scrapy
import string
import time
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request

from TNspider.items import BNUItem

class BnucrawlSpider(scrapy.Spider):
    name = "BNUcrawl"
    allowed_domains = ["bnu.edu.cn"]
    start_urls = (
        'http://career.bnu.edu.cn/JobInfomation.aspx?catid=471',
    )
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.br = webdriver.Chrome()
        
        
    def parse(self, response):
        sel = Selector(response)
        self.br.get(response.url)
        total_pages = "".join(sel.xpath('//div[@id="AspNetPager1"]//a[last()]/@href').extract()).split("'")[-2]
        pagenums = string.atoi(total_pages)
        print pagenums
        for pagenum in range(1,pagenums+1):
            sites = sel.xpath('//dl[@class="ji120101"]//dd')
            follow_url = response.url.split("/")
            follow_url = [follow_url[0],"//",follow_url[2],"/"]
            follow_url ="".join(follow_url)
            for site in sites:
                item = BNUItem()
                item['university'] = "BNU"
                item['city'] = "北京"
                clicks = site.xpath('.//td[3]/text()').extract()
                item['click_times'] = "".join([t.encode('UTF-8') for t in clicks])
                date = site.xpath('.//td[2]/text()').extract()
                item['date'] = [t.encode('UTF-8') for t in date]
                title = site.xpath('.//td[1]/a/text()').extract()
                item['title'] = [t.encode('UTF-8') for t in title]
                link = site.xpath('.//td[1]/a/@href').extract()
                item['link'] = follow_url+"".join([l.encode('UTF-8') for l in link])
                link = follow_url+"".join([l.encode('UTF-8') for l in link])
                yield Request(url=link, meta={'item': item},
                              callback=self.parse_item)
            action_link = self.br.find_element_by_link_text("下一页")
            action_link.click()
            time.sleep(5)
            sel = Selector(text=self.br.page_source)
        self.br.close()
            

    def parse_item(self,response):
        item = response.meta['item']
        sel_detail = Selector(response)
        desc = sel_detail.xpath('//div[@class="i3001 job1list empnr intorone02"]/descendant::text()').extract()
        item['desc'] = [d.encode('UTF-8') for d in desc]
        yield item
