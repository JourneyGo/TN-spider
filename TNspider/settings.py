# -*- coding: utf-8 -*-

# Scrapy settings for TNspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'TNspider'

SPIDER_MODULES = ['TNspider.spiders']
NEWSPIDER_MODULE = 'TNspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TNspider (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
#                  'TNspider.pipelines.TNspiderPipeline':200,
                  'TNspider.pipelines.MysqlPipeline':300,
#                  'scrapy.contrib.pipeline.images.ImagesPipeline': 1
                  }
#Sets delay
DOWNLOAD_DELAY = 0.05
