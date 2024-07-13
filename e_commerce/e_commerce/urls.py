"""
URL configuration for e_commerce project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from e_commerce.store.views import CartViewSet, OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'Product', ProductViewSet)
router.register(r'Cart', CartViewSet)
router.register(r'Order', OrderViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
