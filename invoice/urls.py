from django.urls import path
from . import views


urlpatterns = [
    path('create-invoice/',views.create_invoice,name='create_invoice'),
    path('invoice-item/<int:item_id>/', views.invoice_item_detail, name='invoice-item-detail'),
    path('invoice-items/<int:item_id>/update/', views.update_invoice_item, name='update_invoice_item'),
    path('invoice-items/<int:item_id>/delete/', views.delete_invoice_item, name='delete_invoice_item'),
    path('invoice-item/<str:invoice_id>/customer-name/', views.get_customer_name, name='get_customer_name'),
    path('invoice-item/<str:invoice_id>/update-customer-name/',views. update_customer_name, name='update_customer_name'),
    path('create-invoice-api/',views.create_invoice_api),
    path('invoice/list/',views.invoice_list,name="invoice_list"),
    path('invoice/<str:invoice>/',views.invoice_detail,name="invoice_detail"),
    path('invoice-items/<str:invoice_id>/', views.get_invoice_items, name='invoice-items'),
    path('email-invoice/<str:email>/<str:invoice>/',views.re_email_invoice),
    path('update-payment-method/',views.update_invoice_payment_method),
    path('update-status/', views.update_invoice_status, name='update_invoice_status'),

    # repiirs api enpoints
    # path('get-invoice-number-for-ticket/',views.get_invoice_number_for_ticket),
    path('repair-ticket/invoice/', views.create_invoice_for_ticket, name='create_ticket_invoice_item'),
    path('repair-ticket_invoice_update/<int:pk>/', views.update_invoice_for_ticket, name='update_invoice_for_ticket'),
    path('ticket-invoices/<str:invoice>/',views.get_all_repairs_ticket_invoices_ticket,name="get_all_repairs_ticket_invoices_ticket"),
    path('delete/ticket-item/<int:id>/',views.remove_invoice_item_for_ticket_using_item_id),
    path('update/ticket-invoice/<str:invoice>/',views.update_invoice_for_ticket),
    path("settings/",views.get_settings),
     path('get-customer-email/', views.get_customer_email, name='get_customer_email'),
]

