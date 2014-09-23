# -*- coding: utf-8 -*-

import scrapy
from scrapy.exceptions import CloseSpider
import string
import time
#import calendar
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
import MySQLdb

from TNspider.items import BNUItem

class CAUcrawlSpider(scrapy.Spider):
    name = "DAJIEcrawl"
    allowed_domains = ["dajie.com"]
    start_urls = (
         'http://campus.dajie.com/talk/index',
    )
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.br = webdriver.Chrome()
        print "准备爬取 大街网 宣讲会数据".decode('GBK')
        
    def __del__(self):
        self.br.quit()
        scrapy.Spider.__del__(self)
        
    def parse(self, response):     
        pagenum = 1
###
        # 判重部分1
        newItemsNum = 0;
        firstNewItemFlag = u'1';
        lastLink = self.get_lastCrawl()
#        print lastLink
###        #

        self.br.get('http://campus.dajie.com/talk/index')
        totalButton=self.br.find_element_by_xpath('//*[@id="a-all"]')
        totalButton.click()
        time.sleep(5)
        
        while(True):
            sel = Selector(text = self.br.page_source)
            sites = sel.xpath('//*[@id="J_listContent"]/table/tbody//tr')
            for site in sites:
                if site.xpath('./td[3]/div/a/text()').extract():
                    item = BNUItem()
                else:
                    continue
                title = site.xpath('./td[2]/div/a/text()').extract()
                item['title'] = ''.join([t.encode('UTF-8') for t in title])
                raw_year  = '2014'
                raw_month = site.xpath('./td[1]/div/div[1]/p[1]/text()').extract()
                raw_month = ''.join(raw_month)
                temp_month = '月'.decode('GBK')
                raw_month =  raw_month.split(temp_month)[0]
                raw_month = ''.join([t.encode('UTF-8') for t in raw_month])
                raw_month = string.atoi(raw_month)
                # raw_month = raw_month[0]
                raw_day   = site.xpath('./td[1]/div/div[1]/p[2]/text()').extract()
                raw_day   = ''.join([t.encode('UTF-8') for t in raw_day])
                raw_day   = string.atoi(raw_day)
                date      = raw_year+'-'+('%02d' % raw_month)+'-'+('%02d' % raw_day)
                print date 
                item['date'] = date
                raw_time  = site.xpath('./td[1]/div/div[2]/p[2]/text()').extract()
                raw_time  = ''.join([t.encode('UTF-8') for t in raw_time])
                item['time'] = raw_time
                item['university'] = ''.join([t.encode('UTF-8') for t in site.xpath('./td[3]/div/a/text()').extract()])
                item['addr'] = ''.join([t.encode('UTF-8') for t in site.xpath('./td[4]/div/text()').extract()])
                
                item['city'] = 'TEST' #THIS IS A BIG PROBLEM !
                
                link = ''.join([t.encode('UTF-8') for t in site.xpath('./td[2]/div/a/@href').extract()])
                item['link'] = link

###                
                # 判重部分2
                if item['link'] == lastLink:
                    print "Crawl %d new items"%newItemsNum
                    raise CloseSpider("New Items Crawling Completed")                    
                else:
                    newItemsNum = newItemsNum + 1
                    db = MySQLdb.connect("182.92.10.253","root","thursdaynight","zhaoxuanjiang" )
                    cursor = db.cursor()
                    cursor.execute("UPDATE jobinfo SET flag='0' WHERE flag = '1' && abbreviation = 'DAJIE'")                 
                item['flag'] = firstNewItemFlag
                firstNewItemFlag = u'0';
###                #
                item['abbreviation'] = "DAJIE"
                yield Request(url=item['link'], meta={'item': item},
                              callback=self.parse_item)
                              
            if sel.xpath('//*[@id="maincolumn"]/div[2]/div[2]/div/div/div[2]/div[2]/a[@class="next"]'):
                nextButton = self.br.find_element_by_xpath('//*[@id="maincolumn"]/div[2]/div[2]/div/div/div[2]/div[2]/a[@class="next"]')
                nextButton.click()
                time.sleep(5)
                print pagenum
                pagenum=pagenum+1
            else:
                break
                
                              
                

            
    def parse_item(self,response):
        sel_detail = Selector(response)
        item = response.meta['item']
        item['desc'] = 'desc'#[d.encode('UTF-8') for d in desc]
        item['click_times'] = '0'
        # item['city'] = [d.encode('UTF-8') for d in city]
        # item['title'] = [d.encode('UTF-8') for d in title]
        print "Done!"
        yield item
### 
    #判重部分 3
    def get_lastCrawl(self):
        db = MySQLdb.connect("182.92.10.253","root","thursdaynight","zhaoxuanjiang" )
        #db = MySQLdb.connect("localhost","root","bnulab506mysql","app_jobfair")        
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT * FROM jobinfo WHERE flag = '1' && abbreviation = 'DAJIE'"
        print sql
        # 执行SQL语句
        cursor.execute(sql)
        print "first"
        # 获取所有记录列表
        results = cursor.fetchall()
        #print results
        rowNum = 0
        lastLink = []
        for row in results:  
            rowNum = rowNum + 1
            lastLink = row[6]
            print "lastLink=%s"%lastLink
        db.close() 
        if rowNum > 1:
            raise CloseSpider('Last record is not unique')
        else:
            return lastLink       
        # 关闭数据库连接
          
###