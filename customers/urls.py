from django.urls import path
from . import views


urlpatterns = [
    path('create/',views.customer_create,name="customer_create"),
    path('search/',views.search_customers,name="search_customers"),
    path('details/<int:customer_id>/',views.get_customer_details,name='get_customer_details'),
    path('update/',views.customer_update,name="customer_update"),
]