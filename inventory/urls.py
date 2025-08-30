from django.urls import path
from . import views


urlpatterns = [
    # test
    path("listing/",views.inventory_listing, name="inventory_listing"),
    path("new-item/",views.save_or_update_inventory, name="new_item"),
    # path("inventory-detail/",views.inventory_detail,name="inventory_detail"),
    path("",views.inventory, name="inventory"),
    path("stock-alerts/",views.low_stock_alerts, name="low_stock_alerts"),
    path("barcode-search/",views.barcode_scanner, name="barcode_scanner"),
    path('manage-inventory/',views.manage_inventory, name="manage_inventory"),
    path('add-item/',views.add_item, name="add_item"),
    path('edit-item/item_id',views.edit_item, name="edit_item"),
    path('delete-item/item_id',views.delete_item, name="delete_item"),
    path('expiring-items/',views.expiring_items, name="expiring_items"),


    # suppliers paths
    path('suppliers/', views.supplier_list, name='supplier_list'),  # View all suppliers
    path('suppliers/add/', views.add_supplier, name='add_supplier'),  # Add new supplier
    path('suppliers/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),  # Edit supplier
    path('suppliers/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),  # Delete supplier


    # sales
    path('sales/', views.sales_transactions, name='sales_transactions'),
    path('sales/add/', views.add_sale, name='add_sale'),
    ]