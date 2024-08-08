from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from store.models import Cart
from store.factories import CartFactory, ProductFactory, UserFactory


class StoreAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.product = ProductFactory()

    def test_product_detail(self):
        kwargs = {"id": self.product.id, "slug": self.product.slug}
        url = reverse("product-detail", kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], self.product.name)
        self.assertEqual(response.json()["slug"], self.product.slug)

    def test_product_list(self):
        url = reverse("product-list")
        response = self.client.get(url)
        response_data = response.json()
        print("products", response_data)
        print()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["products"][0]["name"], self.product.name)
        self.assertIsInstance(response_data["products"], list)
        self.assertIsInstance(response_data["categories"], list)

    def test_product_list_by_category(self):
        url = reverse(
            "product-list-by-category",
            kwargs={"category_slug": self.product.category.slug},
        )
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data["products"], list)
        self.assertIsInstance(response_data["categories"], list)
        self.assertIn("category", response_data)


class CartViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.cart = CartFactory(owner=self.user)
        self.other_user = UserFactory()
        self.other_cart = CartFactory(owner=self.other_user)

    def test_cart_list(self):
        url = reverse("cart-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Adjust if more carts are created in setup

    def test_cart_retrieve(self):
        url = reverse("cart-detail", kwargs={"id": self.cart.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.cart.id)

    def test_cart_update(self):
        url = reverse("cart-detail", kwargs={"id": self.cart.id})
        updated_data = {"owner": self.user.id}
        response = self.client.put(url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["owner"], self.user.id)

    def test_cart_delete(self):
        url = reverse("cart-detail", kwargs={"id": self.cart.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(id=self.cart.id).exists())

    def test_cart_add_product(self):
        # Assuming you have a Product model and ProductFactory
        product = ProductFactory()
        url = reverse("cart-add-product")
        data = {"cart_id": self.cart.id, "product_id": product.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn(product, self.cart.products.all())

    def test_cart_remove_product(self):
        # Assuming you have a Product model and ProductFactory
        product = ProductFactory()
        self.cart.products.add(product)
        url = reverse("cart-remove-product")
        data = {"cart_id": self.cart.id, "product_id": product.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(product, self.cart.products.all())

    def test_cart_list_by_user(self):
        pass
