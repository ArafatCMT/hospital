from django.shortcuts import render
from rest_framework import viewsets
from . import models, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class AppointmentPagination(PageNumberPagination):
    page_size = 1 # items per page
    page_size_query_param = page_size 
    max_page_size = 100

class AppointmentViewSet(viewsets.ModelViewSet):
    pagination_class = AppointmentPagination
    permission_classes = [IsAuthenticated]
    queryset = models.Appointment.objects.all()
    serializer_class = serializers.AppointmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset() # 7 no line ke neye aslam ba inherite kore anlam
        
        patient_id = self.request.query_params.get('patient_id')
        # print(patient_id)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        else:
            doctor_id = self.request.query_params.get('doctor_id')
            if doctor_id:
                queryset = queryset.filter(doctor_id=doctor_id)
        return queryset
