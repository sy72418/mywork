from django.db import models

# Create your models here.

class Ordersmodel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default = 0)
    customname = models.CharField(max_length=100)
    customemail = models.CharField(max_length=100)
    customphone = models.CharField(max_length=20)
    customaddress = models.CharField(max_length=200)
    paytype = models.CharField(max_length=20)
    create_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ordersmodel'
    
    

class Detailmodel(models.Model):
    dorder = models.ForeignKey('Ordersmodel',on_delete=models.CASCADE)
    pname = models.CharField(max_length=150)
    unitprice = models.IntegerField()
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'detailmodel'
        
    def __str__(self):
        return self.pname








