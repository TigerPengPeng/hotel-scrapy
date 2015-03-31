#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy import log
from scrapy.spider import Spider
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.selector import Selector
from app.scrapy_manager.models import ScrapyItem
from hotel.items import CityItem
from hotel.util import split_city_href
import datetime
import time

class CityScrapy(Spider):
    name = "ctrip_city"
    allowed_domains = ["ctrip.com"]
    start_urls = [
        "http://hotels.ctrip.com/citylist"
    ]

    def __init__(self, info_log=None): 
        if info_log == None:
            raise NotConfigured("CityScrapy类中: 参数info_log不能为空")
         
        super(CityScrapy, self)
	log.start(logfile=info_log, loglevel=log.INFO, logstdout=False)

	scrapy_item = ScrapyItem()
	scrapy_item.scrapy_name = self.name
	if scrapy_item.is_existed_scrapy_name() is False:
	    scrapy_item.save()

    def parse(self, response):
       sel = Selector(response)
       custom_list = sel.xpath("//div[@class='custom_list']")
       if len(custom_list) == 0:
           raise CloseSpider("城市列表出现解析Exception: 没有解析到sel.xpath(//div[@class='custom_list'])")

       for custom in custom_list:
           group_name = custom.xpath("dt[re:test(., '^[A-Z]$')]/text()").extract()[0].encode("utf-8")
           citys = custom.xpath("dd/a[re:test(@href, '\d$')]")
           if len(citys) == 0:
               raise CloseSpider("城市列表出现解析Exception, 没有解析到custom.xpath(dd/a[re:test(@href, '\d$')])")
               
	   for city in citys:
               href_text = city.xpath("@href").extract()[0][1:].encode("utf-8")
	       name_ch = city.xpath("text()").extract()[0].encode("utf-8")
	       href = "http://hotels.ctrip.com/" + href_text
	       text = href_text.split("/")[-1]
	       list = split_city_href(text)
	       if (list[0] == "" or list[1] == -1):
	           continue
	       name_en = list[0]
	       id = list[1]

	       city_item = CityItem()
               city_item["id"] = id;
               city_item["href"] = href.strip()
               city_item["name_en"] = name_en.strip()
               city_item["name_ch"] = name_ch.strip()
               city_item["group_name"] = group_name
	       log.msg(str(id) + "," + name_ch + "," + name_en + "," + href, level=log.INFO)
	       city_item.save()

    # spider close method
    def closed(self, reason):
        if reason == "finished":
            print "爬虫ctrip_city成功"
        else:
            print "爬虫ctrip_city失败"
            log.msg(reason, level=log.CRITICAL)
