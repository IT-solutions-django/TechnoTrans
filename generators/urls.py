from django.urls import path
from .views import *


app_name = 'generators'


urlpatterns = [
    path('', GeneratorsCatalogView.as_view(), name='catalog'), 
    path('rent/', GeneratorsRentView.as_view(), name='rent'),
    path('<slug:generator_slug>/', GeneratorView.as_view(), name='generator'),
]