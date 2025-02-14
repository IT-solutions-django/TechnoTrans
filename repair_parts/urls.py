from django.urls import path
from .views import *


app_name = 'repair_parts'


urlpatterns = [
    path('', RepairPartsCatalogView.as_view(), name='catalog'), 
     path('<slug:part_slug>/', RepairPartView.as_view(), name='repair_part'),
]