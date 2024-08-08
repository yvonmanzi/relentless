from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from store.models import Cart
from orders.serializers import OrderSerializer
from orders.models import Order


class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    # permission_classes = [IsAuthenticated, IsCartOwner]
    lookup_field = "id"

    # you can only place an order on a cart you own. do we do permissions or just check in the code?
    def place_order(self, request):
        cart_id = request.data["cart_id"]
        customer_id = request.data["customer_id"]
        cart = get_object_or_404(Cart, id=cart_id)
        customer = get_object_or_404(settings.AUTH_USER_MODEL, id=customer_id)

        if cart.owner == customer_id:
            # TODO: We'll return to quantitites later. Same thing as payment and delivery address stuff.
            # for product in cart.products.all():
            #     if product.stock <

            # Create a new order
            order = Order.objects.create(
                cart=cart,
                # quantity=2,  # Number of products ordered
                customer=customer,
                status="placed",  # Optional; default value is 'Pending'
            )

    def retrieve(self, request, id=None):
        pass

    def update(self, request, id=None):
        pass

    def destroy(self, request, id=None):
        pass
