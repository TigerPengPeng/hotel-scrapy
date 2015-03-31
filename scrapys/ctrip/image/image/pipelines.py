# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
import hashlib
from image.util import *
from image.items import HotelImageStaticItem, HotelImageItem

# 处理一个酒店的所有图片
class ImagePipeline(ImagesPipeline):
    def get_image_branch_path(self):
        return "ctrip_images/"

    def get_media_requests(self, item, info):
        self.image_property = "IMAGES_STORE"

	hotel_id = item["hotel_id"]
        hotel_name = item["hotel_name"]
        city_name = item["city_name"]
	image_list = item["images"]

	for image in image_list:
	    url = image["url"]
	    title = image["title"]
	    yield scrapy.Request(url, meta={"city_name":city_name, "hotel_id":hotel_id, "title":title})

    def item_completed(self, results, item, info):
	# 若该酒店没有提供图片, 则直接return
        if len(item["images"]) == 0:
	    return item

        # image_paths 为存储一个酒店所有图片的list
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

	# 记录酒店的图片的统计信息
	hotel_image_static = HotelImageStaticItem()
	hotel_image_static["hotel_id"] = item["hotel_id"]
        hotel_image_static["hotel_name"] = item["hotel_name"]
	hotel_image_static["city_name"] = item["city_name"]
	hotel_image_static["batch_number"] = item["batch_number"]
	hotel_image_static["image_counter"] = len(item["images"])
	hotel_image_static.save()

	# 记录每张图片的信息
	for image_path in image_paths:
	    hotel_image = HotelImageItem()
	    hotel_image["hotel_id"] = item["hotel_id"]
            hotel_image["hotel_name"] = item["hotel_name"]
	    hotel_image["title"] = image_path.split("/")[-1]
	    hotel_image["category"] = image_path.split("/")[-2]
	    hotel_image["image"] = self.get_image_branch_path() + image_path
	    hotel_image.save()
        return item

    def file_path(self, request, response=None, info=None):
	image_guid = request._get_url().split("/")[-1]
        if response != None:
	    city_name = response.meta["city_name"]
	    hotel_id = response.meta["hotel_id"]
	    title = response.meta["title"]
	    return "full/%s/%s/%s/%s" %(city_name, hotel_id, title, image_guid)
	else:
	    return "full/%s.jpg" %(image_guid)
