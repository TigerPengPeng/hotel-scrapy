#coding=utf-8
from django.db import models

# Create your models here.
class HotelProperty(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    name_ch = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.id) + "," + self.name_ch + "," + self.name_en

    class Meta:
        ordering = ['id']


class HotelLocal(models.Model):
    # 酒店id
    hotel_id = models.CharField(max_length=20, db_index=True, editable=False)
    # 酒店的url
    href = models.CharField(max_length=100)
    # 酒店英文名称
    name_en = models.CharField(max_length=200, null=True, blank=True)
    # 酒店中文名称
    name_ch = models.CharField(max_length=200, db_index=True)
    # 酒店电话
    telephone = models.CharField(max_length=60, null=True, blank=True)
    # 传真
    fax = models.CharField(max_length=100, null=True, blank=True)
    # 酒店描述
    des_base = models.TextField(null=True, blank=True)
    # 酒店描述
    des_detail = models.TextField(null=True, blank=True)
    # 国家
    nation = models.CharField(max_length=30)
    # 省份
    province = models.CharField(max_length=30, null=True, blank=True)
    # 城市
    city = models.CharField(max_length=30)
    # 区/县
    location = models.CharField(max_length=30, null=True, blank=True)
    # 酒店中文地址名称
    address = models.TextField()
    # 所在路段
    road_cross = models.TextField(null=True, blank=True)
    # 商业区
    country = models.CharField(max_length=100)
    # 目的地
    destination = models.CharField(max_length=30)
    # 酒店高德地图经纬度
    scott_point = models.CharField(max_length=100, null=True, blank=True)
    # 酒店星级
    star = models.CharField(max_length=10, null=True, blank=True)
    # 酒店评分
    score = models.FloatField()
    # 酒店被点评次数
    review_count = models.IntegerField()
    # 酒店提供的服务
    services = models.CharField(max_length=200, null=True, blank=True)
    # 当前酒店最低的入住价格
    least_price = models.FloatField(null=True, blank=True)
    # 数据入库时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 数据批次号
    batch_number = models.CharField(max_length=20, db_index=True)

    def __unicode__(self):
        return self.hotel_id + "," + self.name_ch

    class Meta:
        ordering = ['id']

    @staticmethod
    def get_hotel_by_id(hotel_id):
        try:
            hotel = HotelLocal.objects.get(hotel_id=hotel_id)
        except HotelLocal.DoesNotExist:
            return None
        else:
            return hotel

    @staticmethod
    def is_existed_hotel_id(hotel_id):
        try:
            HotelLocal.objects.get(hotel_id=hotel_id)
        except HotelLocal.DoesNotExist:
            return False
        else:
            return True

    @staticmethod
    def count_hotel_by_batch_number(batch_number):
        count_number = HotelLocal.objects.filter(batch_number=batch_number).count()
        return count_number

    @staticmethod
    def transfer_ctrip_hote_local(ctrip_hotel):
        local_hotel = HotelLocal()
        local_hotel.hotel_id = ctrip_hotel.hotel_id
        local_hotel.href = ctrip_hotel.href
        local_hotel.name_en = ctrip_hotel.name_en
        local_hotel.name_ch = ctrip_hotel.name_ch
        local_hotel.telephone = ctrip_hotel.telephone
        local_hotel.fax = ctrip_hotel.fax
        local_hotel.des_base = ctrip_hotel.des_base
        local_hotel.des_detail = ctrip_hotel.des_detail
        local_hotel.nation = ctrip_hotel.nation
        local_hotel.province = ctrip_hotel.province
        local_hotel.city = ctrip_hotel.city
        local_hotel.location = ctrip_hotel.location
        local_hotel.address = ctrip_hotel.address
        local_hotel.road_cross = ctrip_hotel.road_cross
        local_hotel.country = ctrip_hotel.country
        local_hotel.destination = ctrip_hotel.destination
        local_hotel.scott_point = ctrip_hotel.scott_point
        local_hotel.star  = ctrip_hotel.star
        local_hotel.score = ctrip_hotel.score
        local_hotel.review_count = ctrip_hotel.review_count
        local_hotel.services = ctrip_hotel.services
        local_hotel.least_price = ctrip_hotel.least_price
        local_hotel.batch_number = ctrip_hotel.batch_number
        return local_hotel

