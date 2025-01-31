from django.contrib import admin
from .models import Customer, Order, OrderItem

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone', 'email', 'registration_date')
    search_fields = ('name', 'code', 'email')
    list_filter = ('registration_date',)
    ordering = ('name',) 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'amount', 'time')
    search_fields = ('customer__name', 'item')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price')
    search_fields = ('order__customer__name', 'item')
