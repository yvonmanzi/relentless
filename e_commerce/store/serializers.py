from rest_framework import serializers

from store.models import Cart, Order, Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Order

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Cart