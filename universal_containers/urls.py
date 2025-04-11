from django.urls import path
from .views import *


app_name = 'universal_containers'


urlpatterns = [
    path('', UniversalCatalogView.as_view(), name='catalog'),
    path('<slug:container_slug>/', UniversalContainerView.as_view(), name='container'),
]