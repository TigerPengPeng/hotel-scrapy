#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import os.path
import scrapy
import time
import datetime
from scrapy import log
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from app.ctrip.models import City, Hotel, HotelReviewStatic
from app.scrapy_manager.models import ScrapyItem, ScrapyBatchItem, SyncScrapyBatchItem
from review.util import *
from review.items import ReviewBaseProperty, HotelReviews


class ReviewScrapy(CrawlSpider):
    name = "ctrip_review"
    allowed_domains = ["ctrip.com"]
    start_urls = [
        "http://hotels.ctrip.com"
    ]
    batch_number = str(time.time())
    scrapy_batch_item = ScrapyBatchItem()

    def __init__(self, cityid=None, info_log=None):
        if info_log == None:
            raise NotConfigured("ReviewScrapy类中: 参数info_log不能为空d")

	super(ReviewScrapy, self)
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

	while(True):
	    if self.cityid == None or self.cityid == "all":
	        hotels = Hotel.objects.all()[skip:skip+limit]
	    else:
	        hotels = Hotel.objects.filter(city=self.city_name)[skip:skip+limit]
	    for hotel in hotels:
	        hotel_id = hotel.hotel_id
		# 判断该酒店的点评是否已经被抓取过
		if HotelReviewStatic.get_hotel_review_static(hotel_id):
		    continue;
		hotel_name = hotel.name_ch
		hotel_href = hotel.href
                city_name = hotel.city
		yield scrapy.Request(parse_review_href(hotel_href),
		meta={"hotel_id":hotel_id, "hotel_name":hotel_name, "city_name":city_name},
		callback=self.parse_review_list)

	    if len(hotels) < limit:
	        break
	    skip = skip + limit

    # 解析点评列表页面
    def parse_review_list(self, response):
        # 酒店点评分页的base url
	base_url = "http://hotels.ctrip.com/hotel/dianping/%s_p%st0.html"
        hotel_id = response.meta["hotel_id"]
	hotel_name = response.meta["hotel_name"]
        city_name = response.meta["city_name"]
	sel = Selector(response)
	page_size = sel.xpath("//div[@class='c_page_list layoutfix']/a[last()]/@value").extract()
	# 酒店没有评论或者酒店只有单页的评论
	if len(page_size) == 0:
	    yield scrapy.Request(base_url %(hotel_id, 1),
	    meta={"hotel_id":hotel_id, "hotel_name":hotel_name, "city_name":city_name},
	    callback=self.parse_review)
	else:
	    total_page = int(list_to_string(page_size, ""))
	    current_page = 1
	    while current_page <= total_page:
	        yield scrapy.Request(base_url %(hotel_id, current_page),
	        meta={"hotel_id":hotel_id, "hotel_name":hotel_name, "city_name":city_name},
	        callback=self.parse_review)
		current_page = current_page + 1

    # 解析单个酒店的点评
    def parse_review(self, response):
        hotel_id = response.meta["hotel_id"]
	hotel_name = response.meta["hotel_name"]
        city_name = response.meta["city_name"]

	sel = Selector(response)
	detail_cmt_box = sel.xpath("//div[@class='detail_cmt_box']")
	comment_block_list = detail_cmt_box.xpath(".//div[@class='comment_block']")
	review_list = []
        hotel_reviews = HotelReviews()
        hotel_reviews["hotel_id"] = hotel_id
        hotel_reviews["hotel_name"] = hotel_name
        hotel_reviews["city_name"] = city_name
        hotel_reviews["batch_number"] = self.batch_number
        hotel_reviews["review_list"] = review_list
	# 若酒店没有点评
	if len(comment_block_list) == 0:
	    return hotel_reviews
	else:
	    for comment_block in comment_block_list:
	        user_info = comment_block.xpath(".//div[@class='user_info']")
		comment_title = comment_block.xpath(".//p[@class='comment_title']")
		comment_adv = comment_block.xpath(".//div[@class='comment_adv']")
		comment_txt = comment_block.xpath(".//div[@class='comment_txt']")
		htl_reply = comment_block.xpath(".//div[@class='htl_reply']")

		customer = list_to_string(user_info.xpath(".//p[@class='name']/span/text()").extract(), "")
		trip = list_to_string(user_info.xpath(".//p[@class='trip']/text()").extract(), "")
		room = list_to_string(user_info.xpath(".//p[@class='room']/text()").extract(), "")

		small_c = list_to_string(comment_title.xpath(".//span[@class='small_c']/@data-value").extract(), "")
		score = list_to_string(comment_title.xpath(".//span[@class='score']/span/text()").extract(), "")
		date = list_to_string(comment_title.xpath(".//span[re:test(@class, '^date')]/a/text()").extract(), "")

		advantages = list_to_string(comment_adv.xpath("p[1]/text()").extract(), "")
		disadvantages = list_to_string(comment_adv.xpath("p[last()]/text()").extract(), "")

		comment_detail = list_to_string(comment_txt.xpath(".//p[@class='J_commentDetail']/text()").extract(), "")
		useful_voted = list_to_string(comment_txt.xpath(".//a[@class='useful useful_voted']/span/text()").extract(), "")

		hotel_reply = list_to_string(htl_reply.xpath(".//p[@class='text']/text()").extract(), "")

		hotel_review = ReviewBaseProperty()
		hotel_review["customer"] = customer
		hotel_review["trip"] = trip
		hotel_review["room"] = room
		hotel_review["review_date"] = date
		hotel_review["score"] = float(score)
		hotel_review["small_c"] = small_c
		hotel_review["advantages"] = advantages
		hotel_review["disadvantages"] = disadvantages
		hotel_review["comment_detail"] = comment_detail
		hotel_review["hotel_reply"] = hotel_reply
		if len(useful_voted) > 0:
		    useful_voted = useful_voted.replace("(", "").replace(")", "")
		    hotel_review["useful_voted"] = int(useful_voted)
		else:
		    hotel_review["useful_voted"] = 0
		review_list.append(hotel_review)

	return hotel_reviews

    def closed(self, reason):
        current_datetime = datetime.datetime.now()
	create_time = datetime.datetime.fromtimestamp(int(self.batch_number.split(".")[0]))

        # update scrapy status
	self.scrapy_batch_item.status = "unexported"
	self.scrapy_batch_item.update_time = current_datetime
	self.scrapy_batch_item.save()

        if reason == "finished":
	    print "爬虫ctrip_review运行成功"
	else:
	    print "爬虫ctrip_review运行失败"
	    log.msg(reason, level=log.CRITICAL)

	summary_text_list = []

	summary_text_list.append("抓取开始时间: " + create_time.strftime("%Y-%m-%d.%H:%M:%S"))
	summary_text_list.append("抓取结束时间: " + current_datetime.strftime("%Y-%m-%d.%H:%M:%S"))

	scrapy_hotels = HotelReviewStatic.count_hotel_by_batch_number(self.batch_number)
	summary_text_list.append("抓取%s家酒店的点评" %(str(scrapy_hotels)))

	file_parent = get_file_path() + "logs"
	file_name = self.info_log.split("/")[-1]
	write_scrapy_summary_log(file_parent, file_name, "\n".join(summary_text_list), "w+")
