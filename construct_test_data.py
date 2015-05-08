#!/usr/bin/env python
# encoding: utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy_project.settings")

from app.ctrip.models import Hotel
import random

if __name__ == "__main__":
    """ Make random data for test
    Bacause data from table which named ctrip_hotel is too large, it's about 22W rows created by file hotel.sql
    But for test, we do not need such big data but we hope that data can be dispersive
    So I wrote this .py file to reduce amount of ctrip_hotel but make it keep dispersive. """
    remove_num = 214000
    for i in range(0, remove_num):
        rm_id = random.randint(225, 215850)
        rm_hotel = Hotel.objects.filter(id=rm_id)
        if len(rm_hotel) is not 0:
            print rm_hotel[0].name_ch
            rm_hotel[0].delete()
