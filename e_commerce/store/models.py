from django.db import models
import uuid
from django.conf import settings

class Address:
    district = models.CharField(max_length=30)
    sector = models.CharField(max_length=30)
    cell = models.CharField(max_length=30)


class PaymentMethod(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('CC', 'Credit Card'),
        ('PP', 'PayPal'),
        ('BT', 'Bank Transfer'),
        ('MM', 'Mobile Money'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPE_CHOICES)
    card_number = models.CharField(max_length=16, blank=True, null=True)  # Only for Credit Card
    paypal_email = models.EmailField(blank=True, null=True)  # Only for PayPal
    bank_account = models.CharField(max_length=20, blank=True, null=True)  # Only for Bank Transfer
    expiry_date = models.DateField(blank=True, null=True)  # Only for Credit Card
    phone_number = models.PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return f'Payment Method {self.id} for {self.customer}'
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'categories'
    def __str__(self) -> str:
        return self.name
# Create your models here.
class Product(models.Model):
    """Model representing a specific product(ie that can be bought)"""

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True)
    # reviews and ratings could potentially be included
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        # Put 'id' and 'slug' together in one index to speed up querries that use both. 
        index_together = (('id', 'slug'), )


    def __str__(self) -> str:
        return self.name


class Cart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='carts',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f' Cart {self.id} for {self.owner}'
    


class Order(models.Model):
    ORDER_STATUS = (
        ('s','SHIPPED'), ('r','ON ROAD'), ('p','PREPARING FOR SHIPPING'), ('rsh','READY FOR SHIPPING'), ('f','FAILED'), ('np','NOT PLACED')
        )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = [models.ForeignKey(Cart, on_delete=models.CASCADE)]
    #TODO: Double check the 'choices'
    status = models.CharField(max_length=3, help_text='Order Status', choices=ORDER_STATUS, default='np')
    date_placed = models.DateField(auto_now_add=True)
    # this should probably not allow blank to true.?
    delivery_date = models.DateField(blank=True, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    delivery_address = models.ManyToManyField(Address)

    def __str__(self) -> str:
        return f'Order {self.id} for {self.customer}'




    


