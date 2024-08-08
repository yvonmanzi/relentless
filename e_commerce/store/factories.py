from django.conf import settings
import factory  # type: ignore
from store.models import Cart, CartItem, Category, Product
from factory.django import DjangoModelFactory  # type: ignore
from django.utils.text import slugify


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("word")  # Generates a random word for the product name
    description = factory.Faker(
        "text", max_nb_chars=200
    )  # Generates a random text for the description
    slug = factory.LazyAttribute(
        lambda o: slugify(o.name)
    )  # Generates a slug from the product name
    image = factory.django.ImageField(
        filename="product_image.jpg"
    )  # Generates a sample image file
    price = factory.Faker(
        "pydecimal", left_digits=6, right_digits=2, positive=True
    )  # Generates a random price
    available = factory.Faker("boolean")  # Random boolean for availability
    created = factory.Faker(
        "date_time_this_year", before_now=True, after_now=False
    )  # Random creation date
    updated = factory.Faker(
        "date_time_this_year", before_now=True, after_now=False
    )  # Random update date


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    owner = factory.SubFactory(UserFactory)  # Create a new User or use an existing one
    created = factory.Faker("date_time_this_year", before_now=True, after_now=False)
    updated = factory.Faker("date_time_this_year", before_now=True, after_now=True)


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)  # Use CartFactory to generate a cart
    product = factory.SubFactory(
        ProductFactory
    )  # Use ProductFactory to generate a product
    quantity = factory.Faker(
        "random_int", min=1, max=10
    )  # Generate a random quantity between 1 and 10
