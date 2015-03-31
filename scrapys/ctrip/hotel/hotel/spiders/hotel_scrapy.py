#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy import log
from scrapy.spider import Spider
from scrapy.selector import Selector
from app.ctrip.models import Hotel
from app.scrapy_manager.models import ScrapyItem, ScrapyBatchItem, SyncScrapyBatchItem 
from hotel.items import CityItem
from hotel.items import HotelItem
import datetime
import time
from hotel.util import *

class HotelScrapy(Spider):
    name = "ctrip_hotel"
    allowed_domains = ["ctrip.com"]
    start_urls = ["http://hotels.ctrip.com"]

    city_entrance_urls = []
    batch_number = str(time.time())
    scrapy_batch_item = ScrapyBatchItem()

    def __init__(self, cityid=None, info_log=None): 
        if info_log == None:
            raise NotConfigured("HotelScrapy类中: 参数info_log不能为空")
        
        super(HotelScrapy, self)
        
        self.info_log = info_log
	log.start(logfile=self.info_log, loglevel=log.INFO, logstdout=False)
	
	if cityid == None or cityid == "all":
            citys = CityItem.django_model.objects.all()
        else:
	    citys = CityItem.django_model.objects.filter(id=cityid)

        if len(citys) == 0:
            raise NotConfigured("参数cityid:" + cityid + "不存在于表city_city中，请检查")
        
        for city in citys:
            self.city_entrance_urls.append(city.href)
         
        if len(self.city_entrance_urls) > 0:
	    scrapy_item = ScrapyItem()
	    scrapy_item.scrapy_name = self.name
	    if scrapy_item.is_existed_scrapy_name() is False:
	        scrapy_item.save()

	    self.scrapy_batch_item.scrapy_name = self.name
	    self.scrapy_batch_item.batch_number = self.batch_number
	    self.scrapy_batch_item.status = "scrapy_running"
	    self.scrapy_batch_item.save()

    # entrance of each city's hotels
    def parse(self, response):
        for city_entrance_url in self.city_entrance_urls:
	    yield scrapy.Request(city_entrance_url, meta = {"url" : city_entrance_url}, callback=self.entrance_parse)
        
    # entrance of each page of one city's hotels 
    def entrance_parse(self, response): 
        sel = Selector(response)
	entrance_url = response.meta["url"]

	total_page_node = sel.xpath("//div[@class='c_page_list layoutfix']/a[last()]/text()")
	if len(total_page_node) > 0:
	    total_page = int(total_page_node.extract()[0])
	else:
            reason = "获取酒店列表页的分页数据失败，请开发人员解决相应问题. 链接为: " + entrance_url 
            log.msg(reason, level=log.CRITICAL)
            raise CloseSpider(reason)
	
	current_page = 1

	while current_page <= total_page: 
	    url = entrance_url + "/p" + str(current_page)
	    current_page = current_page + 1
	    yield scrapy.Request(url, callback=self.hotellist_parse)


    # parse hotel list page and get hotel's href
    def hotellist_parse(self, response):
       sel = Selector(response)
       
       # 抓取酒店列表页的酒店id, 拼接成酒店的url
       hotelid_list = sel.xpath("//div[@class='searchresult_list']/@id[re:test(., '^\d*$')]").extract();
       # 只去抓取数据库中不存在的酒店
       for hotelid in hotelid_list:
	   if Hotel.is_existed_hotel_id(hotelid) is False:
	       hotel_href = "http://hotels.ctrip.com/hotel/" + hotelid + ".html"
	       yield scrapy.Request(hotel_href, callback=self.hotel_parse)

    # parse hotel detail page
    def hotel_parse(self, response):
        sel = Selector(response)
	
	# define nodes
	# 酒店名称 地址 商业区 星级 评分 提供的服务 参考价格
	node_htl_info_com = sel.xpath("//div[contains(@class, 'htl_info_com layoutfix')]")
	# 酒店图片 地图
	node_htl_pic_map = sel.xpath("//div[contains(@class, 'htl_pic_map layoutfix')]")
	# 酒店出售的产品 酒店详细信息 客户评论
	node_main_detail_wrapper = sel.xpath("//div[contains(@class, 'main_detail_wrapper')]")
	# define nodes
	
	hotelid = response.url.split("/")[-1].split(".")[0]

	name_ch = list_to_string(node_htl_info_com.xpath(".//h2[@class='cn_n']/text()").extract(), "") 

	name_en = list_to_string(node_htl_info_com.xpath(".//h2[@class='en_n']/text()").extract(), "")

        address_node = node_htl_info_com.xpath(".//div[@class='adress']")

	city = list_to_string(address_node.xpath(".//span[re:test(@id, 'City$')]/text()").extract(), "")
	
	location = list_to_string(address_node.xpath(".//span[re:test(@id, 'Location$')]/text()").extract(), "")
	
	address = list_to_string(address_node.xpath(".//span[re:test(@id, 'Address$')]/text()").extract(), "")
	
	road_cross = list_to_string(address_node.xpath(".//span[re:test(@id, 'RoadCross$')]/text()").extract(), "")

        country = list_to_string(address_node.xpath(".//a[re:test(@id, '^ctl00_')]/text()").extract(), ",")

	services = list_to_string(node_htl_info_com.xpath(".//div[@class='icon_list']//span/@title").extract(), ",")
	    
	star = list_to_string(node_htl_info_com.xpath(".//div[@class='grade']/span/@title").extract(), "")
	star = parse_hotel_star(star)

	score = list_to_string(node_htl_info_com.xpath(".//span[@class='score']/text()").extract(), "")
	score = parse_hotel_score(score)

	review_count = list_to_string(node_htl_info_com.xpath(".//span[@itemprop='reviewCount']/text()").extract(), "")
	if len(review_count) > 0:
	    review_count = int(review_count)
	else:
	    review_count = 0

	detail = node_main_detail_wrapper.xpath(".//div[@id='htlDes']/p")
	
	des_base = list_to_string(detail.xpath("text()").extract(), "")

	des_detail = list_to_string(detail.xpath(".//span[@itemprop='description']/text()").extract(), "")

	contract_dic = {}
	contract = list_to_string(detail.xpath(".//span[@id='J_realContact']/@data-real").extract(), "")
	contract = contract.split("<a")[0].strip()
	if len(contract) > 0:
	    contract_dic = parse_contract(contract)

	hotel_coordinate = list_to_string(sel.xpath(".//input[@id='hotelCoordinate']/@value").extract(), "")

	hotel = HotelItem()
	hotel["hotel_id"] = hotelid.strip()
	hotel["href"] = response.url
	hotel["name_en"] = name_en.strip()
	hotel["name_ch"] = name_ch.strip()
	if contract_dic.has_key("telephone"):
	    hotel["telephone"] = contract_dic["telephone"].strip()
	if contract_dic.has_key("fax"):
	    hotel["fax"] = contract_dic["fax"].strip()
	hotel["des_base"] = des_base.strip()
	hotel["des_detail"] = des_detail.strip()
	hotel["nation"] = "China"
	hotel["province"] = ""
	hotel["city"] = city
	hotel["location"] = location
	hotel["address"] = address
	hotel["road_cross"] = road_cross
	hotel["country"] = country
	hotel["destination"] = city
	hotel["star"] = star
	hotel["score"] = score
	hotel["review_count"] = review_count
	hotel["services"] = services
	hotel["scott_point"] = hotel_coordinate
	hotel["batch_number"] = self.batch_number

	log.msg(hotel["hotel_id"] + "," + hotel["name_ch"] + "," + hotel["city"] + "," + hotel["href"], level=log.INFO)
	return hotel

    # spider close method
    def closed(self, reason):
        current_datetime = datetime.datetime.now() 
	create_time = datetime.datetime.fromtimestamp(int(self.batch_number.split(".")[0]))

	self.scrapy_batch_item.status = "unexported"
        self.scrapy_batch_item.update_time = current_datetime 
	self.scrapy_batch_item.save()
        if reason == "finished":
            print "爬虫ctrip_hotel成功"
        else:
            print "爬虫ctrip_hotel失败"
            log.msg(reason, level=log.CRITICAL)

	summary_text_list = []

	summary_text_list.append("抓取开始时间: " + create_time.strftime("%Y-%m-%d.%H:%M:%S"))
	summary_text_list.append("抓取结束时间: " + current_datetime.strftime("%Y-%m-%d.%H:%M:%S"))

	scrapy_hotels = Hotel.count_hotel_by_batch_number(self.batch_number)
	summary_text_list.append("新抓取酒店数量: " + str(scrapy_hotels))

	file_parent = get_file_path() + "logs"
	file_name = self.info_log.split("/")[-1]
	write_scrapy_summary_log(file_parent, file_name, "\n".join(summary_text_list), "w+")
