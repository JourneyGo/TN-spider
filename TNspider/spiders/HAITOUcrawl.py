# -*- coding: utf-8 -*-

import scrapy
from scrapy.exceptions import CloseSpider
import string
import time
#import calendar
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import MySQLdb

from TNspider.items import BNUItem

class CAUcrawlSpider(scrapy.Spider):
    name = "HAITOUcrawl"
    allowed_domains = ["haitou.cc"]
    start_urls = (
        'http://xjh.haitou.cc',
    )
                   
    def __init__(self):
        self.cities_dict = {'bj':'北京'.decode('GBK'),'sh':'上海'.decode('GBK'),'gz':'广州'.decode('GBK'),'wh':'武汉'.decode('GBK'),
                       'nj':'南京'.decode('GBK'),'xa':'西安'.decode('GBK'),'cd':'成都'.decode('GBK'),'cq':'重庆'.decode('GBK'),
                       'hf':'合肥'.decode('GBK'),'cs':'长沙'.decode('GBK'),'dl':'大连'.decode('GBK'),'tj':'天津'.decode('GBK'),
                       'hz':'杭州'.decode('GBK'),'jn':'济南'.decode('GBK'),'fz':'福州'.decode('GBK'),'zz':'郑州'.decode('GBK')}
        self.cities = {'bj','sh','gz','wh','nj','xa','cd','cq','hf','cs','dl','tj','hz','jn','fz','zz'}
        scrapy.Spider.__init__(self)
        self.br = webdriver.Chrome()
        print "准备爬取 海投网 宣讲会数据"
        
    def __del__(self):
        self.br.quit()
        scrapy.Spider.__del__(self)
        
    def parse(self, response):
        sel = Selector(response)
        home_url = "http://scc.cau.edu.cn/scc/"       
###
        # 判重部分1
        newItemsNum = 0;
        lastLink = self.get_lastCrawl()
#        print lastLink
###        #

        for city in self.cities:
            urlRq="http://xjh.haitou.cc/%s/uni-0/after/hold/page-1/" % city
            self.br.get(urlRq)
            time.sleep(1)
            sel = Selector(text = self.br.page_source)
            allnewsNumber = [t.encode('UTF-8') for t in sel.xpath('//*[@id="kz-web"]/div[2]/div/div/div[2]/div[2]/h5/span/text()').extract()]
            # print allnewsNumber
            allnewsNumber = string.atoi(''.join(allnewsNumber))
            allpageNumber = allnewsNumber/30
            if (allnewsNumber%30!=0):
                allpageNumber = allpageNumber +1
            for page in range(1,allpageNumber+1):
                sites = sel.xpath('//*[@id="mainInfoTable"]/tbody//tr')
                for site in sites:
                    item = BNUItem()
                    item['city'] = ''.join([t.encode('UTF-8') for t in self.cities_dict[city]])
                    articleLink = ''.join([t.encode('UTF-8') for t in site.xpath('./td[2]/a/@href').extract()])
                    articleLink = 'xjh.haitou.cc'+articleLink
                    # print articleLink
                    
                    thisCrawl = self.get_thisCrawl(articleLink)
                    if thisCrawl > lastLink:
                        newItemsNum = newItemsNum +1
                        item['link'] = 'http://'+articleLink
                        item['flag'] = thisCrawl
                        item['abbreviation'] = 'HAITOU'
                        yield Request(url='http://'+articleLink, meta={'item': item},
                                  callback=self.parse_item)
                                  
                urlRq = "http://xjh.haitou.cc/%s/uni-0/after/hold/page-%d/" % (city,page)
                self.br.get(urlRq)
                time.sleep(1)
                sel = Selector(text = self.br.page_source)
        print '%d NEW ADDED TO DATABASE'  % newItemsNum  
        
    def get_thisCrawl(self,articleLink):
        thisPageID = articleLink.split('.')[-2]
        thisPageID = thisPageID.split('/')[-1]
        thisPageID = string.atoi(thisPageID)
        # print 'THIS PAGE ID IS %d' % thisPageID
        return thisPageID
            
    def parse_item(self,response):
        sel_detail = Selector(response)
        item = response.meta['item']
        desc = sel_detail.xpath('//*[@id="kz-web"]/div[2]/div[1]/div/div[2]/*').extract()
        item['desc'] = [d.encode('UTF-8') for d in desc]
        title =sel_detail.xpath('//*[@id="kz-web"]/div[1]/div[1]/div[1]/h3/text()').extract()
        item['title'] = [d.encode('UTF-8') for d in title]
        university = sel_detail.xpath('//*[@id="kz-web"]/div[1]/div[1]/div[2]/div/div/div[1]/p[1]/span/text()').extract()
        item['university'] = [d.encode('UTF-8') for d in university]
        raw_time = sel_detail.xpath('//*[@id="holdTime"]/text()').extract()
        raw_time = ''.join([d.encode('UTF-8') for d in raw_time])
        raw_time = raw_time.split(' ')
        item['date'] = raw_time[0]
        item['time'] = raw_time[1]
        addr = sel_detail.xpath('//*[@id="kz-web"]/div[1]/div[1]/div[2]/div/div/div[1]/p[3]/span/text()').extract()
        item['addr'] = [d.encode('UTF-8') for d in addr]
        click_times = sel_detail.xpath('//*[@id="kz-web"]/div[1]/div[1]/div[2]/div/div/div[2]/p[3]/span/text()').extract()
        item['click_times'] = [d.encode('UTF-8') for d in click_times]

        # self.br2.get(item['link'])
        # # print 'SUCCESS waiting page to open'
        # # try:
            # # magicbutton = WebDriverWait(self.br2, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='wrapper']/div[4]/div/div")))
        # # except:
            # # print 'FAILED not find button'
            # # pass
        # print 'Step 1 waiting page to open'
        # self.br2.implicitly_wait(2)
        # magicbutton = self.br2.find_element_by_xpath('//*[@id="wrapper"]/div[4]/div/div')
        
        # try:
            # if magicbutton:
                # ActionChains(self.br2).double_click(magicbutton).perform()
                # WebDriverWait(self.br2, 2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="web"]')))
                # print 'SUCCESS click done'
            # else:
                # print 'FAILED Button Not Found'
        # except UnexpectedAlertPresentException:
            # alert = self.br2.switch_to.alert
            # alert.accept()
            # print '!!! alert !!!'
        # except TimeoutException:
            # print '!!!timeout!!!'

        # sel_detail = Selector(text = self.br2.page_source)
            
        link = sel_detail.xpath('//input[@id="frameUrl"]/@value').extract()
        if link:
            link = ''.join([d.encode('UTF-8') for d in link])
            link = link.split('#')[0]
            item['link'] = link
            print 'SUCCESS Link-Updated!'
        else:
            print 'FAILED  No source link ...'
        # item['company']
        # item['fields']
        # print "Done!"
        # print item
        yield item

### 
    #判重部分 3
    def get_lastCrawl(self):
        db = MySQLdb.connect("182.92.10.253","root","thursdaynight","zhaoxuanjiang" )
        # db = MySQLdb.connect("localhost","root","root","jobinfo")        
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # SQL 查询语句
        # sql = "SELECT flag FROM new_table WHERE flag=(select max(flag) from new_table WHERE abbreviation='HAITOU')"
        sql = "SELECT flag FROM jobinfo WHERE flag=(select max(flag) from jobinfo WHERE abbreviation='HAITOU')"
        print sql
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print 'taking data from database :'
        print results
        rowNum = 0
        lastLink = 0
        for row in results:  
            rowNum = rowNum + 1
            lastLink = row[0]
            # print "lastLink=%d"%lastLink
        db.close() 
        return lastLink       
        # 关闭数据库连接
          
###

        
