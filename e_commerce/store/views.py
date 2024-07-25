from rest_framework import viewsets
from rest_framework.decorators import action 
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404

from store.serializers import CartSerializer, OrderSerializer, ProductSerializer

from .models import Cart, Order, Product, Category


#TODO: Will have to add some form of pagination

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(available=True)

    def list (self, request, category_slug=None)-> Response:
        category = None
        products = self.get_queryset()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = self.get_queryset().filter(category=category)
        #TODO: Do you hae to serialize here first?
        # serializer = self.get_serializer(products, many=True)
        return Response({'products': products, 
                            'category': category, 
                            'categories': Category.objects.all()})

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()