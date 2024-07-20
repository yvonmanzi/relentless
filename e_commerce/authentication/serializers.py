from rest_framework import serializers

from authentication.models import Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Customer 
