from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated


from store.permissions import IsCartOwner
from store.serializers import CartSerializer, ProductSerializer, CategorySerializer

from .models import Cart, Product, Category


# TODO: Will have to add some form of pagination


class ProductViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
    lookup_field = "id"

    def retrieve(self, request, id=None, slug=None):
        product = get_object_or_404(Product, id=id, slug=slug)

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def list_by_category(self, request, category_slug=None) -> Response:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

        product_serializer = ProductSerializer(products, many=True)
        category_serializer = CategorySerializer(category)
        categories_serializer = CategorySerializer(Category.objects.all(), many=True)
        response_data = {
            "products": product_serializer.data,
            "categories": categories_serializer.data,
            "category": category_serializer.data,
        }
        return Response(response_data)

    def list(self, request):
        products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        categories_serializer = CategorySerializer(Category.objects.all(), many=True)
        response_data = {
            "products": product_serializer.data,
            "categories": categories_serializer.data,
        }
        return Response(response_data)


# TODO: test permissions for this View
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsCartOwner]
    lookup_field = "id"  # Set the lookup field to 'id'

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            # this one will probably have to change to allow  only admin users.
            permission_classes = [AllowAny]
        elif self.action == [
            "cart_add_product",
            "cart_remove_product",
            "list_by_user",
            "update",
            "destroy",
        ]:
            permission_classes = [IsAuthenticated, IsCartOwner]
        return [permission() for permission in permission_classes]

    def list(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def list_by_user(self, request, user_id=None):
        carts = Cart.objects.filter(owner=user_id)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        print(id)
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
        return Response({"detail": "Cart deleted"}, status=status.HTTP_204_NO_CONTENT)

    def cart_add_product(self, request):
        cart_id = request.data.get("cart_id")
        product_id = request.data.get("product_id")
        if not cart_id or not product_id:
            return Response(
                {"detail": "Both cart_id and product_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart = get_object_or_404(Cart, id=cart_id)
        product = get_object_or_404(Product, id=product_id)
        cart.products.add(product)
        return Response(
            {"detail": "Product added to cart"}, status=status.HTTP_204_NO_CONTENT
        )

    def cart_remove_product(self, request):
        cart_id = request.data.get("cart_id")
        product_id = request.data.get("product_id")
        if not cart_id or not product_id:
            return Response(
                {"detail": "Both cart_id and product_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart = get_object_or_404(Cart, id=cart_id)
        product = get_object_or_404(Product, id=product_id)
        cart.products.remove(product)
        return Response(
            {"detail": "Product removed from cart"}, status=status.HTTP_204_NO_CONTENT
        )
