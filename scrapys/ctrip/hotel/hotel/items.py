# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from app.ctrip.models import City, Hotel


class HotelItem(DjangoItem):
    django_model = Hotel

class CityItem(DjangoItem):
    django_model = City
