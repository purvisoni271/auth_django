from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.conf.urls import url


urlpatterns = [
    # path('api/user-details/', views.user_details, name='user_details'),
    # path('api/verify-login/', views.verify_login, name='verify_login'),
    # path('api/update-profile/<int:pk>/', views.update_profile, name='update_profile'),
    path('api/v1/user-list/', views.UserList.as_view()),
    path('api/v1/user-detail/<int:pk>/', views.UserDetail.as_view()),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api/v1/verify-login/', views.VerifyLogin.as_view(), name='verify_login'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
