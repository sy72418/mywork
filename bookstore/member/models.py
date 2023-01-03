from django.db import models

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=2)
    birthday = models.DateField()
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    create_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'member'