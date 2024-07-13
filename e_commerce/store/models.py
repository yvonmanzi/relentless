from django.db import models
import uuid
from django.conf import settings

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    # reviews and ratings could potentially be included
    image = models.ImageField()
    price = models.FloatField()

    def __str__(self) -> str:
        return self.name

class ProductInstance(models.Model):
    """Model representing a specific product(ie that can be bought)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, blank=True,
                                        help_text='Uniqe id for this particular product across the entire store')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    def __str__(self):
        return f'{self.id} ({self.product.name})'

class Cart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = [models.ForeignKey(ProductInstance, on_delete=models.CASCADE)]

    def __str__(self):
        return f'{self.customer} cart'
    


class Order(models.Model):
    ORDER_STATUS = (
        ('s','SHIPPED'), ('r','ON ROAD'), ('p','PREPARING FOR SHIPPING'), ('rsh','READY FOR SHIPPING'), ('f','FAILED'), ('np','NOT PLACED')
        )

    #TODO: What happens when one product insstance is deleted? how about user? makes sense to delete all the orders
    # associated with the user if he's deleted. so CASCASE is correct here
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = [models.ForeignKey(ProductInstance, on_delete="")]
    #TODO: Double check the 'choices'
    status = models.CharField(max_length=1, help_text='Order Status', choices=ORDER_STATUS, default='np')

    # TODO: double check what blank and null would imply here. 
    date_placed = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        # TODO: A customer can have multiple orders, so might have to thnk of a better str representation.
        return f'{self.customer} order'

    


