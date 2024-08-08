from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from store.factories import ProductFactory


class StoreAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.product = ProductFactory()
    
    def test_product_detail(self):
        # will likely have to use urlencode to encode query param, which is slug in this case. sth like the following:
        # base_url = reverse('product-list')
        # query_params = urlencode({'search': 'widget', 'page': 2})
        # url = f"{base_url}?{query_params}"
        kwargs = {'id': self.product.id, 'slug': self.product.slug}
        print(kwargs)
        url = reverse('product-detail', kwargs=kwargs)
        response = self.client.get(url)
        print(response.json())
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response, self.product.name) # do we need to change response to json first? like this: response.json()?
        self.assertEqual(response.json()['slug'], self.product.slug)
        
        
    def test_product_list(self):
        url = reverse('product-list')  # The name is `product-list` for the list view of ProductViewSet
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response, self.product.name)
        # self.assertIsInstance(response.json(), list)
    
    def test_product_list_by_category(self):
        url =reverse('product-list-by-category', kwargs={'category_slug': self.product.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIsInstance(response.json(), list)


