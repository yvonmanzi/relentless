from django.contrib import admin
from django.db import models
from e_commerce.orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
       model = OrderItem
       raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.AdminModel):
    list_display = ['id', 'customer', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]