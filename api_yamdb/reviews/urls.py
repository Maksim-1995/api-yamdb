from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('titles', views.TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]
