# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from app.ctrip.models import HotelImageStatic, HotelImage

# image base info
class ImageBaseProperty(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()

# hotel's info and hotel's images info
class HotelImages(scrapy.Item):
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    city_name = scrapy.Field()
    batch_number = scrapy.Field()
    images = scrapy.Field()

# single image info
class HotelImageStaticItem(DjangoItem):
    django_model = HotelImageStatic

class HotelImageItem(DjangoItem):
    django_model = HotelImage
