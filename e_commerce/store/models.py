from django.db import models
import uuid
from django.conf import settings

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

    #TODO: What happens when one product insstance is deleted? how about user? makes sense to delete all the orders
    # associated with the user if he's deleted. so CASCASE is correct here
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = [models.ForeignKey(Product, on_delete=models.RESTRICT)]
    #TODO: Double check the 'choices'
    status = models.CharField(max_length=3, help_text='Order Status', choices=ORDER_STATUS, default='np')

    # TODO: double check what blank and null would imply here. 
    date_placed = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        # TODO: A customer can have multiple orders, so might have to thnk of a better str representation.
        return f'{self.customer} order'

    


