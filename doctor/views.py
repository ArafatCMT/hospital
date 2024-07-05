from django.shortcuts import render
from . import models,serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import BaseFilterBackend
from rest_framework.filters import BaseFilterBackend
# Create your views here.

class SingleDoctor(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id:
            return queryset.filter(id = doctor_id)
        return queryset

class DoctorPagination(PageNumberPagination):
    page_size = 1 # items per page
    page_size_query_param = page_size
    max_page_size = 100

class DoctorViewSet(viewsets.ModelViewSet):
    pagination_class = DoctorPagination
    filter_backends = [SingleDoctor]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer

class DesignationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Designation.objects.all()
    serializer_class = serializers.DesignaionSerializer

class SepcializationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SepcializationSerializer

class AvailableTimeForSpecificDoctor(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id:
            return queryset.filter(doctor = doctor_id)
        return queryset


class AvailableTimeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [AvailableTimeForSpecificDoctor]
    queryset = models.AvailableTime.objects.all()
    serializer_class = serializers.AvailableTimeSerializer



class ReviewPagination(PageNumberPagination):
    page_size = 1 # items per page
    page_size_query_param = page_size
    max_page_size = 100


class ReviewsForSpecificDoctor(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id:
            return queryset.filter(doctor = doctor_id)
        return queryset
    
class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = ReviewPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [ReviewsForSpecificDoctor] # ei line e (ReviewsForSpecificDoctor) ei function ta ke call kora hocca
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset() # 7 no line ke inherit kore neye aslam
    #     doctor_id = self.request.query_params.get('doctor_id')
    #     # print(doctor_id)
    #     # print(self.request.query_params)
    #     if doctor_id:
    #         queryset = queryset.filter(doctor_id=doctor_id)
    #     return queryset
