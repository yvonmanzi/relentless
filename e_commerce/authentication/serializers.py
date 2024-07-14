from rest_framework import serializers

from authentication.models import Customer
class CustomerSerializer(serializers.Serializer):
    fields = '__all__'
    model = Customer 
