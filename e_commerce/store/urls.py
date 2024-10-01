from django.urls import path

from store.views import CartViewSet, ProductViewSet

urlpatterns = [
    # TODO: This url needs removing category from the path
    path(
        "products/category/<slug:category_slug>/",
        ProductViewSet.as_view({"get": "list_by_category"}),
        name="product-list-by-category",
    ),
    path(
        "products/<int:id>/<slug:slug>/",
        ProductViewSet.as_view({"get": "retrieve"}),
        name="product-detail",
    ),
    path("products/", ProductViewSet.as_view({"get": "list"}), name="product-list"),
    # list all carts
    path("carts/", CartViewSet.as_view({"get": "list"}), name="cart-list"),
    # carts by a given user.
    # ? why go carts/user vs user/carts. which is one better if any?
    path(
        "carts/user/<int:user_id>/",
        CartViewSet.as_view({"get": "list_by_user"}),
        name="cart-list-by-user",
    ),
    # Retrive a specific cart
    path(
        "carts/<int:id>/", CartViewSet.as_view({"get": "retrieve"}), name="cart-detail"
    ),
    # update or delete a specific cart
    path(
        "carts/<int:id>/",
        CartViewSet.as_view({"put": "update", "delete": "destroy"}),
        name="cart-update-delete",
    ),
    # TODO: Add product to cart, delete from it, checkout cart[aka place an order], etc.
    path(
        "cart_add_product/",
        CartViewSet.as_view({"post": "cart_add_product"}),
        name="cart-add-product",
    ),
    path(
        "cart_remove_product/",
        CartViewSet.as_view({"post": "cart_remove_product"}),
        name="cart-remove-product",
    ),
    path(
        "cart-item-change-quantity/",
        CartViewSet.as_view({"post": "cart_item_change_quantity"}),
        name="cart-item-change-quantity",
    ),
]
