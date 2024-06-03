from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# Register your models here.
admin.site.register(Customer)

# Define a custom admin interface for the Product model and its subclasses
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)



