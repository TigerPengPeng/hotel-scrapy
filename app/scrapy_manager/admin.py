from django.contrib import admin
from app.scrapy_manager.models import * 

# Register your models here.
class ScrapyItemAdmin(admin.ModelAdmin):
    list_display = ('scrapy_name', 'is_enabled')
    search_fields = ('scrapy_name',)


class ScrapyBatchItemAdmin(admin.ModelAdmin):
    list_display = ('scrapy_name', 'status', 'batch_number', 'create_time', 'update_time')
    search_fields = ('scrapy_name', 'status')
    list_filter = ('batch_number',)


class SyncScrapyBatchItemAdmin(admin.ModelAdmin):
    list_display = ('scrapy_name', 'status', 'batch_number', 'create_time', 'update_time')
    search_fields = ('scrapy_name', 'status')
    list_filter = ('batch_number',)

class SendEmailItemAdmin(admin.ModelAdmin):
    list_display = ('receiver_email', 'cc_email', 'type')
    search_fields = ('type',)

admin.site.register(ScrapyItem, ScrapyItemAdmin)
admin.site.register(ScrapyBatchItem, ScrapyBatchItemAdmin)
admin.site.register(SyncScrapyBatchItem, SyncScrapyBatchItemAdmin)
admin.site.register(SendEmailItem, SendEmailItemAdmin)
