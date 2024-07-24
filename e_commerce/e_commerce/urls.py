"""
URL configuration for e_commerce project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import CartViewSet, OrderViewSet, ProductViewSet
# from authentication.views import CustomerViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)
# router.register(r'customers', CustomerViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include("authentication.urls"))
]

