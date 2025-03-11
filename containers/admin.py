from django.contrib import admin
from .models import (
    Brand, 
    ContainerModel,
    ContainerType,
    ContainerImage, 
    Container,
    Category,
    ContainerVideo,
    Compressor,
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


@admin.register(Compressor)
class CompressorModelAdmin(admin.ModelAdmin): 
    list_display = ['name']


class ContainerImageInline(admin.TabularInline): 
    model = ContainerImage 
    extra = 1
    verbose_name = 'Картинка'
    verbose_name_plural = 'Картинки'
    show_change_link = True


class ContainerVideoInline(admin.TabularInline): 
    model = ContainerVideo 
    extra = 1
    verbose_name = 'Видео'
    verbose_name_plural = 'Видео'
    show_change_link = True


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin): 
    list_display = ['name']
    inlines = [
        ContainerImageInline,
        ContainerVideoInline,
    ]
    list_filter = ['categories']
    prepopulated_fields = {'slug': ('name',)}
