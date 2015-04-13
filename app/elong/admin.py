from django.contrib import admin
from app.elong.models import *

# Register your models here.
class HotelPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ch', 'name_en')
    search_fields = ('id', 'name_ch', 'name_en')

class HotelLocalAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'name_ch', 'telephone', 'city', 'address', 'scott_point', 'star', 'href', 'batch_number', 'create_time')
    search_fields = ['hotel_id', 'name_ch', 'city', 'star', 'batch_number']
    list_filter = ('city', 'batch_number')

admin.site.register(HotelProperty, HotelPropertyAdmin)
admin.site.register(HotelLocal, HotelLocalAdmin)
