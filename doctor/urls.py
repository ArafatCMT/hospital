from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('designation', views.DesignationViewSet)
router.register('specialization', views.SepcializationViewSet)
router.register('list', views.DoctorViewSet)
router.register('available_time', views.AvailableTimeViewSet)
router.register('reviews', views.ReviewViewSet)


urlpatterns = [
    path('', include(router.urls))
]