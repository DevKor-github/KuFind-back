from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from person import views


router = DefaultRouter()
router.register('', views.PersonViewSet)

app_name = 'person'

urlpatterns = [
    path('', include(router.urls)),
]