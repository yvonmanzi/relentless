from rest_framework import serializers

from e_commerce.store.models import Cart, Order, Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        name = Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        name = Order

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        name = Cart