from django.db import models

class ScrapyItem(models.Model):
    scrapy_name = models.CharField(max_length=256)
    is_enabled = models.BooleanField(default=True)

    def is_existed_scrapy_name(self):
        try:
	    ScrapyItem.objects.get(scrapy_name=self.scrapy_name)
	except ScrapyItem.DoesNotExist:
            return False
	else:
	    return True

class ScrapyBatchItem(models.Model):
    scrapy_name = models.CharField(max_length=256)
    batch_number = models.CharField(max_length=256)
    status = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)

class SyncScrapyBatchItem(models.Model):
    scrapy_name = models.CharField(max_length=256)
    batch_number = models.CharField(max_length=256)
    status = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)

class SendEmailItem(models.Model):
    receiver_email = models.EmailField()
    cc_email = models.EmailField(null=True)
    type = models.CharField(max_length=30)
