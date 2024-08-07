"""
URL configuration for e_commerce project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from store.views import CartViewSet, ProductViewSet
from orders.views import OrderViewSet

class CustomRouter(DefaultRouter):
    def get_lookup_regex(self, viewset, lookup_prefix=''):
        base_regex = super().get_lookup_regex(viewset, lookup_prefix)
        # Extend the base regex to include the slug
        return f'(?P<{lookup_prefix}id>[^/.]+)/(?P<slug>[^/.]+)'

router = CustomRouter()
router.register(r'products', ProductViewSet, basename='product')


router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
# router.register(r'customers', CustomerViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include("authentication.urls")),
    path('api/', include('store.urls'))
]

