from django.db import models
import uuid
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

class Address(models.Model):
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
    phone_number = PhoneNumberField(blank=True, null=True)

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
    #TODO: Need to review foreign key v one to one so I can use 'related_name' better here. 
    #TODO: Write tests for APIs. 
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f' Cart {self.id} for {self.owner}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, 
        related_name='cart_items', 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
           return str(self.id)
    def get_cost(self):
        return self.product.price * self.quantity




    


