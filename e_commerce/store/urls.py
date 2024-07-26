    
from django.urls import path

from store.views import CartViewSet, ProductViewSet

urlpatterns = [
    #TODO: This url needs removing category from the path
    path('products/<slug:category_slug>/', ProductViewSet.as_view({'get': 'list'}), name='product-list-by-category'),
    # list all carts
    path('carts/', CartViewSet.as_view({'get': 'list'}), name='cart-list'),

    # carts by a given user. 
    #? why go carts/user vs user/carts. which is one better if any?
    path('carts/user/<int:user_id>/', CartViewSet.as_view({'get': 'list_by_user'}), name='cart-list-by-user'),
    # Retrive a specific cart 
    path('carts/<int:id>/', CartViewSet.as_view({'get': 'retrieve'}), name='cart-detail'),
    #update or delete a specific cart
    path('carts/<int:id>/', CartViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='cart-update-delete')
    #TODO: Add product to cart, delete from it, checkout cart[aka place an order], etc. 
    # path('carts/<int:id>/add_product', CartViewSet.as_view({'post': 'add_product'}), name='cart-add-product'),




]


