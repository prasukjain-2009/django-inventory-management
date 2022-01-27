from django.contrib import admin
from django.forms import models
from .models import Manufacturer,ManufacturerContact,Item,Inventory
# Register your models here.

class ManufacturerContactAdmin(admin.StackedInline):
    model = ManufacturerContact

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    def name(self,obj):
        return obj.name
    inlines= (ManufacturerContactAdmin,)
    list_display = ["name","id",]
    list_filter = ["full_name","id",]
    


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["full_name","id",]
    list_filter = ["name","id",]
    


# @admin.register(Manufacturer)
# class ManufacturerAdmin(admin.ModelAdmin):
#     inlines= (ManufacturerContactAdmin,)