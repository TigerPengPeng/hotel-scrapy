# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.exceptions import DropItem
from review.items import ReviewItem, HotelReviewStaticItem, ReviewBaseProperty, HotelReviews
from app.ctrip.models import HotelReviewStatic

class ReviewPipeline(object):
    def process_item(self, item, spider):
        review_list = item["review_list"]
        # if item contains no review
        if len(review_list) == 0:
            return
        else:
            hotel_id = item["hotel_id"]
            review_number = len(review_list)
            hotel_review_static = HotelReviewStatic.get_hotel_review_static(hotel_id)
            # if hotel review static has record part of all
            if hotel_review_static:
                hotel_review_static.add_counter(review_number)
            else:
                # save hotel review static infomation
                hotel_review_static_item = HotelReviewStaticItem()
                hotel_review_static_item["hotel_id"] = hotel_id
                hotel_review_static_item["hotel_name"] = item["hotel_name"]
                hotel_review_static_item["city_name"] = item["city_name"]
                hotel_review_static_item["review_counter"] = review_number
                hotel_review_static_item["batch_number"] = item["batch_number"]
                hotel_review_static_item.save()

                for hotel_review in review_list:
                    review_item = ReviewItem()
                    review_item["hotel_id"] = hotel_id
                    review_item["hotel_name"] = item["hotel_name"]
                    review_item["customer"] = hotel_review["customer"]
                    review_item["trip"] = hotel_review["trip"]
                    review_item["room"] = hotel_review["room"]
                    review_item["review_date"] = hotel_review["review_date"]
                    review_item["score"] = hotel_review["score"]
                    review_item["small_c"] = hotel_review["small_c"]
                    review_item["advantages"] = hotel_review["advantages"]
                    review_item["disadvantages"] = hotel_review["disadvantages"]
                    review_item["comment_detail"] = hotel_review["comment_detail"]
                    review_item["useful_voted"] = hotel_review["useful_voted"]
                    review_item["hotel_reply"] = hotel_review["hotel_reply"]
                    review_item.save()
                    
