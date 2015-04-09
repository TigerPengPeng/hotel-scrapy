# -*- coding: utf-8 -*-

# Scrapy settings for image project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
import sys
from django.conf import settings
# django环境变量相对路径配置
sys.path.append("../../../../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'scrapy_project.settings'

DEFAULT_REQUEST_HEADERS={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en:q=0.8',
    'Connection':'keep-alive',
    'DNT':'1'
}

BOT_NAME = 'image'
DOWNLOAD_DELAY = 2

SPIDER_MODULES = ['image.spiders']
NEWSPIDER_MODULE = 'image.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'image (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'

ITEM_PIPELINES = {
    'image.pipelines.ImagePipeline': 1
}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 543,
}
COOKIES_ENABLED = False
COOKIES_DEBUG = False

IMAGES_STORE = os.path.dirname(os.path.join(settings.MEDIA_ROOT, "ctrip_images/"))

import datetime
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
LOG_STDOUT = False
LOG_FILE = 'logs/error/' + datetime.datetime.now().strftime("%Y-%m-%d.%H") + '.log'
