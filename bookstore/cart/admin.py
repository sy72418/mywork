from django.contrib import admin

# Register your models here.

from cart import models

class ordersadmin(admin.ModelAdmin):
    list_display = ('customname','customemail','grandtotal','paytype','create_date')


admin.site.register(models.Ordersmodel,ordersadmin)
admin.site.register(models.Detailmodel)