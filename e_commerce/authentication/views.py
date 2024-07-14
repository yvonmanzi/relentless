from django.shortcuts import render
from rest_framework import viewsets

from authentication.models import Customer
from authentication.serializers import CustomerSerializer

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    class Meta:
        serializer_class = CustomerSerializer
        queryset = Customer.objects.all()