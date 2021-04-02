from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='ProductView'),
    # path('', views.index, name='index'),
    # path('', views.PaypalFormView.as_view(), name='PaypalFormView'),
    path('paypal-return/', views.PaypalReturnView.as_view(), name='paypal-return'),
    path('paypal-cancel/', views.PaypalCancelView.as_view(), name='paypal-cancel'),
    path('subscribe/', views.subscription, name='subscription'),
    path('process_subscription/', views.process_subscription, name='process_subscription'),
]
