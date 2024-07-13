from django.shortcuts import render
from rest_framework import viewsets

from store.serializers import CartSerializer, OrderSerializer, ProductSerializer

from .models import Cart, Order, Product


# Create your views here.
#TODO: Will have to add some form of pagination
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()