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
