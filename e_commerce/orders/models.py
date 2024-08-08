from django.conf import settings
from django.db import models
from store.models import PaymentMethod, Address, Cart, Product


class Order(models.Model):
    ORDER_STATUS = (
        ("p", "placed"),
        ("s", "SHIPPED"),
        ("r", "ON ROAD"),
        ("p", "PREPARING FOR SHIPPING"),
        ("rsh", "READY FOR SHIPPING"),
        ("f", "FAILED"),
        ("np", "NOT PLACED"),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO: Double check the 'choices'
    status = models.CharField(
        max_length=3, help_text="Order Status", choices=ORDER_STATUS, default="np"
    )
    date_placed = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    # this should probably not allow blank to true.?
    delivery_date = models.DateField(blank=True, null=True)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True
    )
    delivery_address = models.ManyToManyField(
        Address,
    )
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-date_placed",)

    def __str__(self) -> str:
        return f"Order {self.id} for {self.customer}"

    def get_total_cost(self):
        return sum(order_item.get_cost() for order_item in self.items.all())


class OrderItem(models.Model):
    cart = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.price * self.quantity
