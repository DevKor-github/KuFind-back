from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from object import views


router = DefaultRouter()
router.register('', views.ObjectViewSet)

app_name = 'object'

urlpatterns = [
    path('', include(router.urls)),
]