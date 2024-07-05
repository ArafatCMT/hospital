from django.shortcuts import render
from rest_framework import viewsets
from . import models,serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class ContactUsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializer
