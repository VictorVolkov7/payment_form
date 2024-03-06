from django.contrib import admin

from products.models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('name', 'total_price',)
