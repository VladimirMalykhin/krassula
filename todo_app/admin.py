# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.html import format_html
from django.contrib import admin
from .models import *

class OrdersAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		return False
	
class ProductAdmin(admin.ModelAdmin):

    readonly_fields = ["photo1"]
    search_fields = ["name"]
    list_filter = ["category"]

    def photo1(self, obj):
        return format_html('<p><img src="{url}" id="photo-admin" width="350" height=210 /><img src="{url2}" style="margin-left:50px" id="photo-big-admin" width=auto height=210 /></p>'.format(
            url = obj.photo,
            url2 = obj.big_photo,
            )
    )  

class CategoryAdmin(admin.ModelAdmin):

    readonly_fields = ["photo1"]

    def photo1(self, obj):
        return format_html('<p><img src="{url}" id="photo-admin" width="350" height=210 /></p>'.format(
            url = obj.photo.url,
            )
    ) 
    
# Register your models here.
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Child_Categories)
admin.site.register(Products, ProductAdmin)
admin.site.register(News)
admin.site.register(Manufacturer)
admin.site.register(Filter)
admin.site.register(Analyz)
admin.site.register(Site_Feedback)
admin.site.register(Products_Feedback)
admin.site.register(Prais)
admin.site.register(Measurements)
admin.site.register(Orders, OrdersAdmin)
