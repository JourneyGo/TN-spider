# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 15:38:16 2014
@author: xzd
Last modified @ 2014 
"""

import scrapy
from scrapy.exceptions import CloseSpider
#import string
import time
#import calendar
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
import MySQLdb

from TNspider.items import BNUItem

class CAUcrawlSpider(scrapy.Spider):
    university = "CAU"
    name = "CAUcrawl"
    allowed_domains = ["cau.edu.cn"]
    start_urls = (
        'http://scc.cau.edu.cn/scc/index.php?pageId=1&mid=35&do=fairlist',
    )
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.br = webdriver.Chrome()
        print u"准备爬取 中国农业大学 宣讲会数据"
    def __del__(self):
        self.br.quit()
        scrapy.Spider.__del__(self)
        
    def parse(self, response):
        sel = Selector(response)
        home_url = "http://scc.cau.edu.cn/scc/"       
        pagenum = 1
###
        # 判重部分1
        newItemsNum = 0;
        firstNewItemFlag = u'1';
        lastLink = self.get_lastCrawl()
#        print lastLink
###        #
        for page in range(1,pagenum+1):
            urlRq="http://scc.cau.edu.cn/scc/index.php?pageId=%d&mid=35&do=fairlist" % page
            self.br.get(urlRq)
            time.sleep(1)
            sel = Selector(text = self.br.page_source)
            sites = sel.xpath('//*[@id="mainArea"]/div[2]/table/tbody/tr[2]/td/table/tbody/tr')
            for site in sites[1:]:
                item = BNUItem()
                title = site.xpath('.//td[1]/a/text()').extract()
                item['title'] = ''.join([t.encode('UTF-8') for t in title])
                print title[0][1:3]
                if title[0][1:3] == u"校外":
                    continue
                item['title'] = [t.encode('UTF-8') for t in title]
                item['date'] = site.xpath('.//td[2]/text()').extract()
                print item['date']
                link = site.xpath('.//td[1]/a/@href').extract()
                # print link
                item['link'] = home_url+"".join([l.encode('UTF-8') for l in link])
###                
                # 判重部分2
                if item['link'] == lastLink:
                    print "Crawl %d new items"%newItemsNum
                    raise CloseSpider("New Items Crawling Completed")                    
                else:
                    newItemsNum = newItemsNum + 1
                    db = MySQLdb.connect("182.92.10.253","root","thursdaynight","zhaoxuanjiang" )
                    cursor = db.cursor()
                    cursor.execute("UPDATE jobinfo SET flag='0' WHERE flag = '1' && abbreviation = 'CAU'")                 
                item['flag'] = firstNewItemFlag
                firstNewItemFlag = u'0';
###                #
                item['university'] = "中国农业大学"
                item['abbreviation'] = "CAU"
                item['city'] = "北京"
                yield Request(url=item['link'], meta={'item': item},
                              callback=self.parse_item)
            
    def parse_item(self,response):
        sel_detail = Selector(response)
        item = response.meta['item']
        desc = sel_detail.xpath('//*[@id="mainArea"]/*').extract()
        item['desc'] = [d.encode('UTF-8') for d in desc]
        print "Done!"
        yield item
### 
    #判重部分 3
    def get_lastCrawl(self):
        #db = MySQLdb.connect("localhost","root","bnulab506mysql","app_jobfair")        
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT * FROM jobinfo WHERE flag = '1' && abbreviation = 'CAU'"
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

        
