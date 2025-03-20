from django.contrib import admin
from .models import (
    Brand, 
    RepairPart, 
    RepairPartImage,
    RepairPartCategory,
)


# class RepairPartImage(admin.TabularInline): 
#     model = RepairPartImage 
#     extra = 1
#     verbose_name = 'Картинка'
#     verbose_name_plural = 'Картинки'
#     show_change_link = True


# @admin.register(RepairPart)
# class RepairPartAdmin(admin.ModelAdmin): 
#     list_display = ['name']
#     inlines = [RepairPartImage,]
#     prepopulated_fields = {'slug': ('name',)}


# @admin.register(RepairPartCategory)
# class RepairPartCategoryAdmin(admin.ModelAdmin): 
#     list_display = ['name']
