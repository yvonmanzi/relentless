import factory  # type: ignore
from store.models import Category, Product
from factory.django import DjangoModelFactory # type: ignore
from django.utils.text import slugify

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.Faker('word') 
    slug = factory.LazyAttribute(lambda o: slugify(o.name)) 

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker('word')  # Generates a random word for the product name
    description = factory.Faker('text', max_nb_chars=200)  # Generates a random text for the description
    slug = factory.LazyAttribute(lambda o: slugify(o.name))  # Generates a slug from the product name
    image = factory.django.ImageField(filename='product_image.jpg')  # Generates a sample image file
    price = factory.Faker('pydecimal', left_digits=6, right_digits=2, positive=True)  # Generates a random price
    available = factory.Faker('boolean')  # Random boolean for availability
    created = factory.Faker('date_time_this_year', before_now=True, after_now=False)  # Random creation date
    updated = factory.Faker('date_time_this_year', before_now=True, after_now=False)  # Random update date
    


