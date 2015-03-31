# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from app.ctrip.models import HotelReview, HotelReviewStatic

class ReviewItem(DjangoItem):
    django_model = HotelReview

class HotelReviewStaticItem(DjangoItem):
    django_model = HotelReviewStatic

# 酒店评论的基本属性
class ReviewBaseProperty(scrapy.Item):
    customer = scrapy.Field()
    trip = scrapy.Field()
    room = scrapy.Field()
    review_date = scrapy.Field()
    score = scrapy.Field()
    small_c = scrapy.Field()
    advantages = scrapy.Field()
    disadvantages = scrapy.Field()
    comment_detail = scrapy.Field()
    useful_voted = scrapy.Field()
    hotel_reply = scrapy.Field()

# 一个酒店的单面的所有评论
class HotelReviews(scrapy.Item):
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    city_name = scrapy.Field()
    batch_number = scrapy.Field()
    review_list = scrapy.Field()
