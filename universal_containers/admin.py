from django.contrib import admin
from containers.models import (
    ContainerModel, 
    ContainerType, 
    Brand
)
from .models import (
    UniversalContainer, 
    UniversalContainerImage,
    UniversalContainerVideo
)


class UniversalContainerImageInline(admin.TabularInline): 
    model = UniversalContainerImage 
    extra = 1
    verbose_name = 'Картинка'
    verbose_name_plural = 'Картинки'
    show_change_link = True


class UniversalContainerVideoInline(admin.TabularInline): 
    model = UniversalContainerVideo 
    extra = 1
    verbose_name = 'Видео'
    verbose_name_plural = 'Видео'
    show_change_link = True


@admin.register(UniversalContainer)
class UniversalContainerAdmin(admin.ModelAdmin): 
    list_display = ['name']
    inlines = [
        UniversalContainerImageInline,
        UniversalContainerVideoInline,
    ]
    list_filter = ['categories']
    prepopulated_fields = {'slug': ('name',)}