from django.urls import path, include
from rest_framework import routers

from .views import (
    CommentViewSet,
    ReviewViewSet,
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    api_signup,
    api_token
)


v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', api_signup, name='signup'),
    path('v1/auth/token/', api_token, name='token'),
    path('v1/', include(v1_router.urls)),
]
