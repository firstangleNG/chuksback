from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "part_name", "sku", "barcode", "category", "supplier_name", 
        "quantity_available", "low_stock_threshold", "reorder_level", 
        "cost_price", "selling_price", "location", "expiration_date", "updated_at"
    )
    list_filter = ("category", "supplier_name", "location")
    search_fields = ("part_name", "sku", "barcode", "supplier_name")
    ordering = ("part_name",)
    readonly_fields = ("updated_at",)
