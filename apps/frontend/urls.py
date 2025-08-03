from django.urls import path
from . import views

urlpatterns = [
    path('', views.SubscriptionListView.as_view(), name='home'), 
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscription-list'),
    path('plans/', views.PlanListView.as_view(), name='plans'),
    path('exchange/', views.ExchangeRateView.as_view(), name='exchange'),
    
]