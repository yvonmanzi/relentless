from django.contrib import admin

from store.models import Address, Cart, PaymentMethod, Product, Category


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["owner", "display_products"]

    def display_products(self, obj):
        return ", ".join([product.name for product in Product.objects.all()])

    display_products.short_description = "Products"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "available", "created", "updated"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "payment_type",
        "paypal_email",
        "bank_account",
        "phone_number",
        "card_number",
    ]
    list_filter = ["customer", "phone_number", "paypal_email"]
    list_editable = ["phone_number", "paypal_email"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["district", "sector", "cell"]
    list_filter = ["sector", "cell", "district"]
    list_editable = ["cell", "sector"]
