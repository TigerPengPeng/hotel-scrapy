from django.contrib import admin
from app.ctrip.models import * 

# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ch', 'name_en', 'group_name', 'href')
    search_fields = ('id', 'name_ch', 'name_en')
    list_filter = ('group_name',)

class TaiWanCityAdmin(admin.ModelAdmin):
    list_display = ('city_id', 'is_taiwan')

class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'name_ch', 'telephone', 'city', 'address', 'scott_point', 'star', 'href', 'batch_number', 'create_time')
    search_fields = ['hotel_id', 'name_ch', 'city', 'star', 'batch_number']
    list_filter = ('city', 'batch_number')

class SyncHotelAdmin(admin.ModelAdmin):
   list_display = ('hotel', 'status', 'result', 'batch_number', 'create_datetime') 
   search_fields = ('status',) 
   list_filter = ('batch_number',)


class PropertyRelationAdmin(admin.ModelAdmin):
    list_display = ('hotel_property', 'name_ch')
    search_fields = ('name_ch',)


class HotelImageStaticAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'hotel_name', 'city_name', 'image_counter', 'batch_number')
    search_fields = ('hotel_id', 'hotel_name', 'city_name', 'batch_number')
    list_filter = ('batch_number',)


class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'hotel_name', 'title', 'category', 'image')
    search_fields = ('hotel_id', 'hotel_name', 'category')


class HotelReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'hotel_name', 'comment_detail', 'trip', 'room', 'score', 'small_c', 'advantages', 'disadvantages')
    search_fields = ('hotel_id', 'hotel_name')

class HotelReviewStaticAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'hotel_name', 'city_name', 'review_counter', 'batch_number')
    search_fields = ('hotel_id', 'hotel_name', 'city_name', 'batch_number')
    list_filter = ('batch_number', )


admin.site.register(City, CityAdmin)
admin.site.register(TaiWanCity, TaiWanCityAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(SyncHotel, SyncHotelAdmin)
admin.site.register(PropertyRelation, PropertyRelationAdmin)
admin.site.register(HotelImageStatic, HotelImageStaticAdmin)
admin.site.register(HotelImage, HotelImageAdmin)
admin.site.register(HotelReview, HotelReviewAdmin)
admin.site.register(HotelReviewStatic, HotelReviewStaticAdmin)
