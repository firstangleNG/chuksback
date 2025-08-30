from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("users.urls")),
    path('repairs/',include("repairs.urls")),
    path('inventory/',include("inventory.urls")),
    path('api/customers/',include("customers.urls")),
    path('invoicing/',include('invoice.urls')),
    path('dashboard/',include('dashboard.urls')),
]
