from rest_framework import viewsets
from rest_framework.decorators import action 
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404

from store.serializers import CartSerializer, OrderSerializer, ProductSerializer, CategorySerializer

from .models import Cart, Order, Product, Category


#TODO: Will have to add some form of pagination

class ProductViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(available=True)

    def retrieve(self, request, id=None):
        # get 'slug' from the Url
        slug = request.query_params.get('slug')
        product = get_object_or_404(Product,
                                   id=id,
                                   slug=slug,
                                   available=True)
        serializer = self.get_serializer(product)
        return Response(serializer.data)
        

    def list (self, request, category_slug=None)-> Response:
        category = None
        products = self.get_queryset()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = self.get_queryset().filter(category=category)
         # Serialize data
        product_serializer = self.get_serializer(products, many=True)
        category_serializer = CategorySerializer(category) if category else None
        categories_serializer = CategorySerializer(Category.objects.all(), many=True)
        response_data = {'products': product_serializer.data, 
                            'categories': categories_serializer.data}
        if category_serializer:
            response_data['category'] = category_serializer.data 
        return Response(response_data)
        
            

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class CartViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def list_by_user(self, request, user_id=None):
        carts = Cart.objects.filter(owner_id=user_id)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        cart = get_object_or_404(Cart, id=id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def update(self, request, id=None):
        cart = get_object_or_404(Cart, id=id)
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, id=None):
        cart = get_object_or_404(Cart, id=id)
        cart.delete()
        return Response(status=204)
    
