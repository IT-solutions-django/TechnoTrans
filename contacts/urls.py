from django.urls import path
from .views import *


app_name = 'contacts'


urlpatterns = [
    path('about-company/', AboutCompanyView.as_view(), name='about_company'),
]