from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscription_retrieve.as_view(), name='subscription_retrieve'),
    path('create-subscription-session/<str:price_id>/', views.create_subscription_session, name='create_subscription_session'),
]
