from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'phone',
        'city',
        'pincode',
        'total_price',
        'payment_method',
        'status',
        'created_at'
    )

    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('full_name', 'phone', 'city', 'pincode')
