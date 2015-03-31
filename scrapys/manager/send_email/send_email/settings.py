# -*- coding: utf-8 -*-

# Scrapy settings for send_email project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import sys
sys.path.append("../../../../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'scrapy_project.settings'

BOT_NAME = 'send_email'

SPIDER_MODULES = ['send_email.spiders']
NEWSPIDER_MODULE = 'send_email.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'send_email (+http://www.yourdomain.com)'

import datetime
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
LOG_STDOUT = False
LOG_FILE = 'logs/error/' + datetime.datetime.now().strftime("%Y-%m-%d.%H") + '.log'
