from rest_framework import serializers

from store.models import Cart, Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category
