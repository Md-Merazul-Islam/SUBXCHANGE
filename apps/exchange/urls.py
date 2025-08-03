
from django.urls import path
from .import views
urlpatterns = [
    path('exchange-rate/', views.ExchangeRateAPIView.as_view(), name='exchange-rate'),
    path('exchange-rate/history/', views.ExchangeRateHistoryAPIView.as_view(), name='exchange-rate-history'),
]
