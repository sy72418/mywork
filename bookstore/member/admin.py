from django.contrib import admin

# Register your models here.

from .models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name','sex','birthday','email','create_date')
    
admin.site.register(Member,MemberAdmin)