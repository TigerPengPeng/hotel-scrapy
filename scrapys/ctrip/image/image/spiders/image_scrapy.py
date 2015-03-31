#coding=utf-8
import sys 
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import os.path
import scrapy
import hashlib
import time
import datetime
from scrapy import log
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from image.items import ImageBaseProperty, HotelImages
from image.util import *
from app.ctrip.models import City, TaiWanCity, Hotel, HotelImageStatic
from app.scrapy_manager.models import ScrapyItem, ScrapyBatchItem, SyncScrapyBatchItem


class ImageScrapy(CrawlSpider):
    name = "ctrip_image"
    allowed_domains = ["ctrip.com"]
    start_urls = [
        "http://hotels.ctrip.com"
    ]
    batch_number = str(time.time())
    scrapy_batch_item = ScrapyBatchItem()

    def __init__(self, cityid=None, info_log=None):
        if info_log == None:
            raise NotConfigured("ImageScrapy类中: 参数info_log不能为空d")

	super(ImageScrapy, self)
	self.info_log = info_log
	if cityid == None or cityid == "all":
	    self.cityid = cityid
	else:
	    city = City.get_city_by_id(cityid)
	    if city == None: 
	        raise NotConfigured("参数cityid:" + cityid + "不存在于表city_city中，请检查")
	    else:
	        self.cityid = cityid
	        self.city_name = city.name_ch

	log.start(logfile=info_log, loglevel=log.INFO, logstdout=False)

	# store scrapy
	scrapy_item = ScrapyItem()
	scrapy_item.scrapy_name = self.name
	if scrapy_item.is_existed_scrapy_name() is False:
	    scrapy_item.save()
	# record scrapy status
	self.scrapy_batch_item.scrapy_name = self.name
	self.scrapy_batch_item.batch_number = self.batch_number
	self.scrapy_batch_item.status = "scrapy_running"
	self.scrapy_batch_item.save()
	
    def parse(self, response):
        limit = 1000
	skip = 0
	base_url = "http://hotels.ctrip.com/Domestic/tool/AjaxLoadPictureAlbum.aspx?hotel=%s&city=%s&istaiwan=%s"
	
	while(True):
	    if self.cityid == None or self.cityid == "all":
	        hotels = Hotel.objects.all()[skip:skip+limit]
	    else:
	        hotels = Hotel.objects.filter(city=self.city_name)[skip:skip+limit]
	    for hotel in hotels:
		hotel_id = hotel.hotel_id
		# 判断该酒店的图片是否已经被抓取过
		if HotelImageStatic.get_hotel_image_static(hotel_id):
		    log.msg("hotel_id为%s的酒店图片已经被抓取过" %(hotel_id), level=log.INFO)
		    continue
		hotel_name = hotel.name_ch
		# 获取城市信息，判断是否为台湾城市
		city = City.get_city_by_name_ch(hotel.city)
		if city == None:
		    continue
		city_id = city.id
		is_taiwan = TaiWanCity.is_taiwan_city(city_id) 
		city_name = city.name_ch
		yield scrapy.Request(base_url %(hotel_id, city_id, is_taiwan), 
		meta={"hotel_id":hotel_id, "city_name":city_name, "hotel_name":hotel_name}, 
		callback=self.parse_image_url)

	    if len(hotels) < limit:
	        break
	    skip = skip + limit

    # return one hotel's images infomation
    def parse_image_url(self, response):
	city_name = response.meta["city_name"]
	hotel_id = response.meta["hotel_id"]
	hotel_name = response.meta["hotel_name"]

	sel = Selector(response)
	images = sel.xpath("//a[re:test(@class, '^pic_s')]")

	image_list = []
	hotel_images = HotelImages()
	hotel_images["hotel_id"] = hotel_id
	hotel_images["hotel_name"] = hotel_name
	hotel_images["city_name"] = city_name
	hotel_images["batch_number"] = self.batch_number
	hotel_images["images"] = image_list
	# 每次循环获得单个酒店一张图片的属性
	for image in images:
	    image_base_property = ImageBaseProperty()
	    href = image.xpath(".//img/@data-bigpic").extract()
	    title = image.xpath(".//span/text()").extract()
	    href = list_to_string(href, "")
	    title = list_to_string(title, "")
	    
	    if title == "":
	        image_base_property["title"] = "缺少分类"
	    else:
		image_base_property["title"] = title
            
	    image_format = href.split(".")[-1]
            image_base_property["url"] = href.split("_")[0] + "." + image_format

	    image_list.append(image_base_property)

	log.msg(hotel_id + "," + hotel_name + "," + city_name + "," + str(len(image_list)) + "张图片", level=log.INFO)
	return hotel_images

    def closed(self, reason):
        current_datetime = datetime.datetime.now()
	create_time = datetime.datetime.fromtimestamp(int(self.batch_number.split(".")[0]))

        # update scrapy status
	self.scrapy_batch_item.status = "unexported"
	self.scrapy_batch_item.update_time = current_datetime
	self.scrapy_batch_item.save()

        if reason == "finished":
	    print "爬虫ctrip_image运行成功"
	else:
	    print "爬虫ctrip_image运行失败"
	    log.msg(reason, level=log.CRITICAL)

	summary_text_list = []

	summary_text_list.append("抓取开始时间: " + create_time.strftime("%Y-%m-%d.%H:%M:%S"))
	summary_text_list.append("抓取结束时间: " + current_datetime.strftime("%Y-%m-%d.%H:%M:%S"))

	scrapy_hotels = HotelImageStatic.count_hotel_by_batch_number(self.batch_number) 
	summary_text_list.append("抓取%s家酒店的图片" %(str(scrapy_hotels)))

	file_parent = get_file_path() + "logs"
	file_name = self.info_log.split("/")[-1]
	write_scrapy_summary_log(file_parent, file_name, "\n".join(summary_text_list), "w+")
