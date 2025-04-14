from django.urls import path
from .views import *


app_name = 'home'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('api/save-request/', SaveRequestView.as_view(), name='save_request'),
    path('api/save-calculate-request/', SaveCalculateRequestView.as_view(), name='save_calculate_request'),
    path('api/save-cargo-request/', SaveCargoTransportationRequestView.as_view(), name='save_cargo_request'),

    path('test-404/', Test404View.as_view()),
]