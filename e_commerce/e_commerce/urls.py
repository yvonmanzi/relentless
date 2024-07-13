"""
URL configuration for e_commerce project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import CartViewSet, OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
