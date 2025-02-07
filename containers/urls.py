from django.urls import path
from .views import *


app_name = 'containers'


urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
]