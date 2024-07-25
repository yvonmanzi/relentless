    
from django.urls import path

from store.views import ProductViewSet

urlpatterns = [
    path('products/category/<slug:category_slug>/', ProductViewSet.as_view({'get': 'list'}), name='product-list-by-category'),
]


