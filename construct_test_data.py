#!/usr/bin/env python
# encoding: utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy_project.settings")

from app.ctrip.models import Hotel
from app.elong.models import HotelLocal
import random

def transfer_hotel(hotel_local):
    hotel = Hotel()
    hotel.hotel_id = hotel_local.hotel_id
    hotel.href = hotel_local.href
    hotel.name_en = hotel_local.name_en
    hotel.name_ch = hotel_local.name_ch
    hotel.telephone = hotel_local.telephone
    hotel.fax = hotel_local.fax
    hotel.des_base = hotel_local.des_base
    hotel.des_detail = hotel_local.des_detail
    hotel.nation = hotel_local.nation
    hotel.province = hotel_local.province
    hotel.city = hotel_local.city
    hotel.location = hotel_local.location
    hotel.address = hotel_local.address
    hotel.road_cross = hotel_local.road_cross
    hotel.country = hotel_local.country
    hotel.destination = hotel_local.destination
    hotel.scott_point = hotel_local.scott_point
    hotel.star  = hotel_local.star
    hotel.score = hotel_local.score
    hotel.review_count = hotel_local.review_count
    hotel.services = hotel_local.services
    hotel.least_price = hotel_local.least_price
    hotel.batch_number = hotel_local.batch_number
    return hotel


if __name__ == "__main__":
    """ Make random data for test
    Bacause data from table which named ctrip_hotel is too large, it's about 22W rows created by file hotel.sql
    But for test, we do not need such big data but we hope that data can be dispersive
    So I wrote this .py file to reduce amount of ctrip_hotel but make it keep dispersive. """
    counter = 0
    while counter <= 1000:
        random_id = random.randint(1, 604863)
        try:
            hotel_local = HotelLocal.objects.get(id=random_id)
            hotel = transfer_hotel(hotel_local)
            hotel.save()
            print hotel.name_ch
            counter += 1
        except HotelLocal.DoesNotExist:
            continue

