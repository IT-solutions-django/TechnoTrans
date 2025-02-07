from django.contrib import admin
from .models import (
    Brand, 
    ContainerModel,
    ContainerType,
    ContainerImage, 
    Container,
    Category,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(ContainerType)
class ContainerTypeAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(ContainerModel)
class ContainerModelAdmin(admin.ModelAdmin): 
    list_display = ['name']


class ContainerImageInline(admin.TabularInline): 
    model = ContainerImage 
    extra = 1
    verbose_name = 'Картинка'
    verbose_name_plural = 'Картинки'


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin): 
    list_display = ['name']
    inlines = [ContainerImageInline,]
    prepopulated_fields = {'slug': ('name',)}