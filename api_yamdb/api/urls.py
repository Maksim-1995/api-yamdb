from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, api_signup, api_token


v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', api_signup, name='signup'),
    path('v1/auth/token/', api_token, name='token'),
    path('v1/', include(v1_router.urls)),
]
