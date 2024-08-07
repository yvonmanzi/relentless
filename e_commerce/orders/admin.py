from django.contrib import admin
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
       model = OrderItem
       raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'paid', 'date_placed', 'date_updated']
    list_filter = ['paid', 'date_placed', 'date_updated']
    inlines = [OrderItemInline]