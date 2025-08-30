from django.urls import path
from . import views 


urlpatterns = [
    # path("tickets/",views.ticket_list,name="ticket_list"),
    path('tickets/<uuid:user_id>/', views.ticket_list, name='ticket_list'),
    path('add/',views.add_ticket,name="add_ticket"),
    path('properties/',views.getAllPropertyData,name="getAllPropertyData"),
    path('summary/<int:id>/<str:tk>/',views.ticket_summary,name="ticket_summary"),
    #  path('summary/',views.ticket_summary,name="ticket_summary"),
    path("tickets/create/",views.create_repair_ticket),
    path("ticket/<str:ticket_id>/update/", views.update_ticket_status, 
    name="update_ticket_status"), 
    path("ticket/<str:ticket_id>/update/detail/", views.ticket_update, 
    name="ticket_update"), 
    path('ticket-detail/<str:ticket_id>/',views.ticket_detail),
    path("set-technician/",views.set_technician),
    path('note/<str:ticket_id>/', views.get_repair_ticket_notes, name='get-ticket-notes'),
    path('note/create/<str:ticket_id>/', views.create_repair_ticket_note, name='create-ticket-note'),
    path('properties/', views.property_list, name='property-list'),
    path('properties/create/', views.property_create, name='property-create'),
    path('properties/<int:pk>/', views.property_detail, name='property-detail'),
    path('properties/<int:pk>/update/', views.property_update, name='property-update'),
    path('properties/<int:pk>/delete/', views.property_delete, name='property-delete'),
    path("email-tickets/", views.email_tickets, name="email_tickets"),
    path('customer-email/',views.get_customer_email),

    # payment

     path('payments/', views.payment_list_create, name='payment-list-create'),
     path('payments/amount-due/<str:ticket_id>/', views.get_amount_due, name='count_payments'),
    # path('payments/<str:ticket>/',views. payment_detail, name='payment-detail'),
     path('payments/delete/<int:payment_id>/', views.delete_payment, name='delete-payment'),
     path('description/add/',views.add_description)

]
 
