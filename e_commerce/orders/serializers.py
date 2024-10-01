from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.Serializer):
    class Meta:
        fields = "__all__"
        model = Order
