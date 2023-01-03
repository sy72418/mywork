from django.db import models

# Create your models here.

class goods(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150)
    publish_date = models.DateField()
    price = models.IntegerField()
    img_url = models.CharField(max_length=250)
    link_url = models.CharField(max_length=300)
    
    class Meta:
        db_table = 'goods'