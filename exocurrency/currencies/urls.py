from django.conf import settings
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin

from .views import CurrencyRateListAPIView, CurrencyExchangeAPIView, TimeWeightedRateReturnAPIView


urlpatterns = [
    path('rates/', CurrencyRateListAPIView.as_view(), name='rates'),
    path('exchange/<str:base>/<str:target>/<int:amount>/', CurrencyExchangeAPIView.as_view(), name='exchanges'),
    path('time-weighted-rate/<str:base>/<str:target>/<int:amount>/', TimeWeightedRateReturnAPIView.as_view(), name='time_weighted_rate'),
]
