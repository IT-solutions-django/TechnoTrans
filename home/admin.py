from django.contrib import admin
from .models import Request, CalculatePriceRequest, ServiceType
from. filters import IsClosed


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin): 
    list_display = ['name', 'phone', 'created_at', 'is_closed']
    list_filter = [
        IsClosed
    ]


@admin.register(CalculatePriceRequest)
class CalculatePriceRequestAdmin(admin.ModelAdmin): 
    list_display = ['city', 'phone', 'created_at', 'is_closed']
    list_filter = [
        IsClosed
    ]


@admin.register(ServiceType)
class RequestAdmin(admin.ModelAdmin): 
    list_display = ['name']