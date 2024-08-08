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
        kwargs = {'id': self.product.id, 'slug': self.product.slug}
        url = reverse('product-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.product.name) 
        self.assertEqual(response.json()['slug'], self.product.slug)
        
        
    def test_product_list(self):
        url = reverse('product-list') 
        response = self.client.get(url)
        response_data = response.json()
        print('products', response_data)
        print()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['products'][0]['name'], self.product.name)
        self.assertIsInstance(response_data['products'], list)
        self.assertIsInstance(response_data['categories'], list)
    
    def test_product_list_by_category(self):
        url =reverse('product-list-by-category', kwargs={'category_slug': self.product.category.slug})
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data['products'], list)
        self.assertIsInstance(response_data['categories'], list)
        self.assertIn('category', response_data)


