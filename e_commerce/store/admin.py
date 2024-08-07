from django.contrib import admin

from store.models import Cart, Product, Category


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['owner', 'display_products']
    def display_products(self, obj):
        return ', '.join([product.name for product in Product.objects.all()])
    display_products.short_description = 'Products'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}