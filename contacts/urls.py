from django.urls import path
from .views import *


app_name = 'contacts'


urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about-company/', AboutCompanyView.as_view(), name='about_company'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('documentation/', DocumentationView.as_view(), name='documentation'),
]