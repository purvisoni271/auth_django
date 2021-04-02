from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('config/', views.stripe_config),
    path('create-checkout-session/<str:product_id>/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    # path('webhook/', views.stripe_webhook),
    path('pricing_page/', views.pricing_page, name='pricing_page'),
]
