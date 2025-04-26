from django.contrib import admin

# Register your models here.
from .models import MenuItem, Order, OrderItem

# Inline model to show OrderItems inside the Order admin view
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# Custom admin for Orders
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestamp', 'status']
    list_filter = ['status']
    inlines = [OrderItemInline]

# Simple registration for MenuItem and OrderItem
admin.site.register(MenuItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)