"""
URL configuration for e_commerce project.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from store.views import CartViewSet, ProductViewSet
from orders.views import OrderViewSet


router = DefaultRouter()
router.register(r"carts", CartViewSet, basename="cart")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"products", ProductViewSet, basename="product")
# router.register(r'customers', CustomerViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("authentication.urls")),
    path("api/", include("store.urls")),
]
