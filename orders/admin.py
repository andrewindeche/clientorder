from django.contrib import admin
from .models import Customer, Order, OrderItem

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code','phone','email', 'registration_date')
    search_fields = ('name', 'code', 'email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'amount', 'time', 'status', 'payment_method')
    search_fields = ('customer__name', 'item', 'status', 'payment_method')
    list_filter = ('status', 'payment_method')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price')
    search_fields = ('order__customer__name', 'item')
