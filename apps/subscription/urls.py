from django.urls import path

from . import views

urlpatterns = [

    # Plans
    path("plans/create/", views.PlanCreateAPIView .as_view(), name=""),
    path('plans/', views.PlanListAPIView.as_view(), name='plan-list'),
  
    # Subscriptions
    path('subscribe/', views.SubscriptionCreateAPIView.as_view(), name='subscribe'),
    path('list/', views.UserSubscriptionListAPIView.as_view(), name='user-subscriptions'),
    path('list/<int:pk>/', views.SubscriptionDetailAPIView.as_view(), name='subscription-detail'),
    path('cancel/<int:subscription_id>/', views.SubscriptionCancelAPIView.as_view(), name='cancel-subscription'),


    # all subscription list
    path('', views.AllSubscriptionsAPIView.as_view(), name='all-subscriptions'),
    
]