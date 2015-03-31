#coding=utf-8
from django.db import models
from app.elong.models import HotelProperty

class City(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    href = models.CharField(max_length=100)
    name_en = models.CharField(max_length=20)
    name_ch = models.CharField(max_length=40, db_index=True)
    group_name = models.CharField(max_length=1)

    @staticmethod
    def get_city_by_id(city_id):
        city_list = City.objects.filter(id=city_id)
	if len(city_list) == 0:
	    return None
	else:
	    return city_list[0]

    @staticmethod
    def get_city_by_name_ch(name_ch):
        city_list = City.objects.filter(name_ch=name_ch)
	if len(city_list) == 0:
	    return None
	else:
	    return city_list[0]

    def __unicode__(self):
        return str(self.id) + "\t" + self.name_en + "\t" +self. name_ch + "\t" + self.href

    class Meta:
        ordering = ['group_name']

class TaiWanCity(models.Model):
    city_id = models.IntegerField(db_index=True, primary_key=True)
    is_taiwan = models.IntegerField()

    @staticmethod
    def is_taiwan_city(city_id):
        try:
	    city = TaiWanCity.objects.get(city_id=city_id)
	except TaiWanCity.DoesNotExist:
	    return 0
	else:
	    return city.is_taiwan

class Hotel(models.Model):
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
	    hotel = Hotel.objects.get(hotel_id=hotel_id)
	except Hotel.DoesNotExist:
	    return None
	else:
            return hotel

    @staticmethod
    def is_existed_hotel_id(hotel_id):
        try:
	    Hotel.objects.get(hotel_id=hotel_id)
	except Hotel.DoesNotExist:
	    return False
	else:
            return True

    @staticmethod
    def count_hotel_by_batch_number(batch_number):
        count_number = Hotel.objects.filter(batch_number=batch_number).count()
	return count_number


# record hotels have been exported
class SyncHotel(models.Model):
    hotel = models.ForeignKey(Hotel, db_index=True)
    batch_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    result = models.TextField(null=True, blank=True)
    create_datetime = models.DateTimeField(auto_now_add=True)

# record ctrip-elong property relation
class PropertyRelation(models.Model):
    hotel_property = models.ForeignKey(HotelProperty, db_index=True, primary_key=True)
    name_ch = models.CharField(max_length=50)


# record hotel image static information
class HotelImageStatic(models.Model):
    hotel_id = models.CharField(max_length=20, db_index=True)
    hotel_name = models.CharField(max_length=200, db_index=True)
    city_name = models.CharField(max_length=40, db_index=True)
    image_counter = models.IntegerField()
    batch_number = models.CharField(max_length=20, db_index=True)

    @staticmethod
    def count_hotel_by_batch_number(batch_number):
        count_number = HotelImageStatic.objects.filter(batch_number=batch_number).count()
	return count_number

    @staticmethod
    def get_hotel_image_static(hotel_id):
        try:
	    hotel_image_static = HotelImageStatic.objects.get(hotel_id=hotel_id)
	except HotelImageStatic.DoesNotExist:
	    return None
	else:
	    return hotel_image_static
    class Meta:
        ordering = ["city_name", "hotel_id"]



# record hotel image information
class HotelImage(models.Model):
    hotel_id = models.CharField(max_length=20, db_index=True)
    hotel_name = models.CharField(max_length=200, db_index=True)
    title = models.CharField(max_length=128, null=True, blank=True, db_index=True)
    category = models.CharField(max_length=128, null=True, blank=True, db_index=True)
    image = models.ImageField(upload_to="ctrip_images", max_length=512)



# record hotel review static
class HotelReviewStatic(models.Model):
    hotel_id = models.CharField(max_length=20, db_index=True)
    hotel_name = models.CharField(max_length=200, db_index=True)
    city_name = models.CharField(max_length=40, db_index=True)
    review_counter = models.IntegerField()
    batch_number = models.CharField(max_length=20, db_index=True)
    @staticmethod
    def count_hotel_by_batch_number(batch_number):
        count_number = HotelReviewStatic.objects.filter(batch_number=batch_number).count()
	return count_number

    @staticmethod
    def get_hotel_review_static(hotel_id):
        try:
	    hotel_review_static = HotelReviewStatic.objects.get(hotel_id=hotel_id)
	except HotelReviewStatic.DoesNotExist:
	    return None
	else:
	    return hotel_review_static

    def add_counter(self, add_counter_value):
        self.review_counter = self.review_counter + add_counter_value
        self.save()

    class Meta:
        ordering = ["city_name", "hotel_id"]



# record hotel reviews
class HotelReview(models.Model):
    hotel_id = models.CharField(max_length=20, db_index=True)
    hotel_name = models.CharField(max_length=200, db_index=True)
    customer = models.CharField(max_length=64, null=True, blank=True)
    trip = models.CharField(max_length=64, null=True, blank=True)
    room = models.CharField(max_length=64, null=True, blank=True)
    review_date = models.CharField(max_length=64, null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    small_c = models.CharField(max_length=64, null=True, blank=True)
    advantages = models.CharField(max_length=128, null=True, blank=True)
    disadvantages = models.CharField(max_length=128, null=True, blank=True)
    comment_detail = models.TextField(null=True, blank=True)
    useful_voted = models.IntegerField(null=True, blank=True)
    hotel_reply = models.TextField(null=True, blank=True)
