from django.contrib import admin
from app.elong.models import HotelProperty

# Register your models here.
class HotelPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ch', 'name_en')
    search_fields = ('id', 'name_ch', 'name_en')


admin.site.register(HotelProperty, HotelPropertyAdmin)
