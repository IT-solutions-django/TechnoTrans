from django.contrib import admin
from .models import (
    Generator, 
    GeneratorCategory, 
    GeneratorPower, 
    GeneratorType,
    GeneratorImage,
)


class GeneratorImageInline(admin.TabularInline): 
    model = GeneratorImage 
    extra = 1
    verbose_name = 'Картинка'
    verbose_name_plural = 'Картинки'
    show_change_link = True


@admin.register(Generator)
class RepairPartAdmin(admin.ModelAdmin): 
    list_display = ['name']
    inlines = [GeneratorImageInline,]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GeneratorCategory)
class RepairPartCategoryAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(GeneratorPower)
class GeneratorPowerAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(GeneratorType)
class GeneratorTypeAdmin(admin.ModelAdmin): 
    list_display = ['name']