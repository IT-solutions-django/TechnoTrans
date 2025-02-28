from django.urls import path
from .views import *


app_name = 'containers'


urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('rent/', ContainersRentView.as_view(), name='rent'),
    path('<slug:container_slug>/', ContainerView.as_view(), name='container'),

]