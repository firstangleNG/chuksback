
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvoiceItemSerializer
from .models import InvoiceItem
import logging
from decimal import Decimal
from django.contrib.auth.decorators import login_required


logger = logging.getLogger('django')

from invoice.models import InvoiceItem
# @login_required(login_url='/')
def generate_invoice_number():
    # Get the latest invoice and increment by 1
    last_invoice = InvoiceItem.objects.order_by('-invoice').first()

    # Ensure the invoice exists and is a valid numeric string
    if last_invoice and last_invoice.invoice and last_invoice.invoice.isdigit():
        new_number = int(last_invoice.invoice) + 1
    else:
        new_number = 1

    # Return a 6-digit invoice number (e.g., 000001)
    return f"{new_number:06}"

@api_view(['GET'])
# @login_required(login_url='/')
def get_invoice_number_for_ticket(request):
    invoice = generate_invoice_number()
    return Response(data={'invoice':invoice},status=status.HTTP_200_OK)


# # @login_required(login_url='/')


# from django.core.exceptions import ValidationError
# @api_view(['GET', 'POST'])
# def create_invoice(request):
#     if request.method == "POST":
#         # Extract data from the request
#         invoice = request.data.get('invoice_number')  # Adjusted for the form data
#         customer_name = request.data.get('customer_name')
#         service_names = request.data.get('items', [])  # Now it's a list of item details
#         payment_status = request.data.get('payment_status')
#         payment_method = request.data.get('payment_method')

#         # Validate required fields (existing validation logic)
#         if not invoice or not customer_name:
#             return Response({"error": "Invoice number and Customer Name are required."}, status=status.HTTP_400_BAD_REQUEST)
#         if not service_names:
#             return Response({"error": "At least one item is required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Process each service item and create InvoiceItem objects
#         for item in service_names:
#             try:
#                 invoice_item = InvoiceItem(
#                     invoice=invoice,
#                     payment_status=payment_status,
#                     payment_method=payment_method,
#                     customer_name=customer_name,
#                     service_name=item['service_name'],
#                     description=item['description'],
#                     quantity=int(item['quantity']),
#                     price_per_unit=float(item['price_per_unit']),
#                     taxes=float(item['tax']),
#                 )
#                 # Save the item to the database
#                 invoice_item.save()
#             except ValidationError as e:
#                 return Response({"error": f"Invalid data for service item: {e.message}"}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Return success message with the created invoice items
#         return Response({"success": True, "message": "Invoice successfully created."}, status=status.HTTP_201_CREATED)
#     else:
#         invoice = generate_invoice_number()
#         return render(request, 'invoice.html', {"invoice": invoice})




from django.shortcuts import render, get_object_or_404
from .models import InvoiceItem
# @login_required(login_url='/')
def invoice_list(request):
    # Fetching all invoices grouped by the 'invoice' field
    invoices = InvoiceItem.objects.values(
        'invoice'
    ).distinct().order_by('-invoice')

    # Collecting additional details by fetching the first item for each invoice
    detailed_invoices = [
        InvoiceItem.objects.filter(invoice=invoice['invoice']).first()
        for invoice in invoices
    ]

    return render(request, 'invoice_list.html', {'invoices': detailed_invoices})


# @login_required(login_url='/')
def invoice_detail(request, invoice):
    # Fetching all items related to a specific invoice
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)

    # Ensure at least one item exists, or return 404
    if not invoice_items.exists():
        return get_object_or_404(InvoiceItem, invoice=invoice)

    # Use the first item to display general information
    invoice_first = invoice_items.first()

    total_amount,final_tax = getAllTotals(invoice=invoice)

    return render(request, 'invoice_detail.html', {"invoice":invoice_first,"invoices":invoice_items,"subtotal":Decimal(total_amount)-Decimal(final_tax),'final_amount':total_amount,"final_tax":final_tax})


@api_view(['POST'])
# @login_required(login_url='/')
def create_invoice_items(request):
 
    items = request.data.get('items', [])
    
    # If no items were provided in the request
    if not items:
        return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)
    # Iterate over the array of items and create InvoiceItem objects
    invoice_items = []
    for item in items:
        # Calculate the total for the item before saving
        item['total'] = (item['quantity'] * item['price_per_unit']) + item['taxes']
        serializer = InvoiceItemSerializer(data=item)
        
        if serializer.is_valid():
            serializer.save()
            invoice_items.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(invoice_items, status=status.HTTP_201_CREATED)


from repairs.models import RepairTicket
@api_view(['POST'])
# @login_required(login_url='/')
def create_invoice_for_ticket(request):
    # Extract the item data from the request body

    item = request.data.copy()  
    ticket_id = item.get("ticket_id")  # Ensure ticket_id is provided

    if not ticket_id:
        logger.error("Ticket id not provided")
        return Response({"error": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate required fields
    invoice = item.get("invoice", "").strip()
    invoice_existed = True  # Flag to check if invoice already existed

    if not invoice:
        logger.info("Invoice not provided, generating a new one.")
        invoice = generate_invoice_number()
        invoice_existed = False  # Mark as newly generated

    # Find the ticket by ticket_id
    ticket = get_object_or_404(RepairTicket, ticket_id=ticket_id)

    # Assign the invoice and save the ticket
    ticket.invoice = invoice
    ticket.save()
    customer_name = f"{ticket.customer.first_name} {ticket.customer.last_name}" # Get the customer's name from the Repair ticket 

    item["invoice"] = invoice  # Ensure invoice is included in the item
    item['customer_name'] = customer_name 


    ticket_id = item.pop("ticket_id", None)  # Remove ticket_id if it exists
    
    # Create a serializer instance with the incoming data
    serializer = InvoiceItemSerializer(data=item)

    # Validate and save the item if it's valid
    if serializer.is_valid():
        serializer.save()
        response_data = serializer.data
        
        # Only return the invoice if it was newly generated
        if not invoice_existed:
            response_data["invoice"] = invoice

        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.db.models import Sum
def getAllTotals(invoice):
    totals = InvoiceItem.objects.filter(invoice=invoice).aggregate(
        finalTotal=Sum('total'),
        totalTax=Sum('tax_amount')
    )
    return totals['finalTotal'] or 0.00, totals['totalTax'] 

 

@api_view(['GET'])
# @login_required(login_url='/')
def get_all_repairs_ticket_invoices_ticket(request, invoice):
    try:
        invoiceitems_instance = InvoiceItem.objects.filter(invoice=invoice)

        # Serialize the data
        serializer = InvoiceItemSerializer(invoiceitems_instance, many=True)
        
        # Ensure both values are Decimal for multiplication
        # total_amount, total_tax  = getAllTotals(invoice)
        total_amount,final_tax = getAllTotals(invoice=invoice)

        return Response({
            "data": serializer.data,
            "subtotal":Decimal(total_amount)-Decimal(final_tax),
            "total_amount": total_amount,
            "final_tax": final_tax
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f'Error : {e}', exc_info=True)  # Log with traceback
        return Response({"error": f"Error : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['PATCH'])
# @login_required(login_url='/')
def update_invoice_for_ticket(request, invoice):
    try:
        # Extract the items array from the request body
        items = request.data.get('items', [])

        # Fetch all invoice items for the given ticket_id
        invoice_items = InvoiceItem.objects.filter(invoice=invoice)

        if not invoice_items.exists():
            logger.error("No invoice items found for the invoice number ")
            return Response({"error": f"No invoice items found for invoice {invoice}."}, status=status.HTTP_404_NOT_FOUND)

        updated_items = []

        # Iterate through the invoice items and update them
        for invoice_item, item_data in zip(invoice_items, items):
            invoice_item.service_name = item_data.get('service_name', invoice_item.service_name)
            invoice_item.description = item_data.get('description', invoice_item.description)
            invoice_item.quantity = item_data.get('quantity', invoice_item.quantity)
            invoice_item.price_per_unit = item_data.get('price_per_unit', invoice_item.price_per_unit)
            invoice_item.taxes = item_data.get('taxes', invoice_item.taxes)

            # Save the item (total is calculated automatically in the model's save() method)
            invoice_item.save()

            # Collect updated data for response
            updated_items.append({
                "service_name": invoice_item.service_name,
                "description": invoice_item.description,
                "quantity": invoice_item.quantity,
                "price_per_unit": invoice_item.price_per_unit,
                "taxes": invoice_item.taxes,
                "total": invoice_item.total,  # This reflects the updated value
            })

        return Response({
            "message": "Invoice items updated successfully.",
            "invoice": invoice,
            "updated_items": updated_items
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"error occured : {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(["DELETE"])
# @login_required(login_url='/')
def remove_invoice_item_for_ticket_using_item_id(request, id):
    try:
        invoice_item = InvoiceItem.objects.get(id=id)
        invoice_item.delete()
        return Response({"message": "Invoice item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except InvoiceItem.DoesNotExist:
        return Response({"error": "Invoice item not found."}, status=status.HTTP_404_NOT_FOUND)
    


from .models import Settings
from .serializers import SettingsSerializer
@api_view(["GET"])
def get_settings(request):
    try:
        settings = Settings.objects.all()
        if not settings.exists(): 
            return Response(data={"settings": []}, status=status.HTTP_200_OK)  
        serializer = SettingsSerializer(settings, many=True)
        return Response(data={"settings": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return Response(data={"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 


from .views import getAllTotals
from .tasks import send_email_invoice
from babel.numbers import format_currency
@api_view(["POST"])
def email_invoice(request):
    name = request.data.get("customer_name")
    email = request.data.get("email")
    invoice = request.data.get('invoice')
    print(invoice)

    if not name:
        logger.error(f"Error occurred: Customer name is not found in request ")
        return Response(data={"error": "Customer name must be entered"}, status=status.HTTP_400_BAD_REQUEST)
    

    if not email:
        logger.error(f"Error occurred: email is not found in request data")
        return Response({"error": "Email address must be entered"}, status=status.HTTP_400_BAD_REQUEST)

    
        #  Get all invoice items for the particular invoice number linked to the invoice  number    
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)
    if len(invoice_items) < 1:
        logger.error(f"Error occurred: Invalid invoice number {invoice}")
        return Response({"error": "Invalid Invoice  Number"}, status=status.HTTP_400_BAD_REQUEST)
    # Create a list of all the invoice items to be passed to the template
    items_list = []
    for item in invoice_items:
        items_list.append({
            'customer_name':item.customer_name,
            'invoice':item.invoice,
            'created_at':item.created_at,
            "service_name": item.service_name,
            "description": item.description,
            "quantity": item.quantity,
            "price_per_unit": str(item.price_per_unit),
            "taxes": str(item.taxes),
            "tax_amount": str(item.tax_amount),
            "total_price": str(item.total),
            "payment_method": item.get_payment_method_display(),
            "payment_status": item.payment_status,
        })

    # Get all Total for Invoice 
    grand_total,total_tax = getAllTotals(invoice=invoice)
    gbp_formatted_grand_total = format_currency(grand_total, 'GBP', locale='en_GB')
    gbp_formatted_total_tax = format_currency(total_tax, 'GBP', locale='en_GB')
    gbp_formatted_subtotal = format_currency(Decimal(grand_total) - Decimal(total_tax)
, 'GBP', locale='en_GB') 
    try:
        scheme = request.scheme
        host = request.get_host()
        endpoint = f"{scheme}://{host}"

        # Async email task
        send_email_invoice.delay_on_commit(
            endpoint=endpoint,
            email=email,
           invoices={
                "invoices": items_list , # Pass all invoice items to the email template
                "subtotal" : gbp_formatted_subtotal,
                "grand_total": gbp_formatted_grand_total, 
                "total_tax": gbp_formatted_total_tax,
                "email" :email,
                "name":name
            }               
        )

        return Response({"message": "Email is being sent"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def create_invoice(request):
    if request.method == 'POST':
        invoice = request.POST.get('invoice')  
        customer_name = request.POST.get('customer_name')
        service_names = request.POST.getlist('service_name[]')
        descriptions = request.POST.getlist('description[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('price_per_unit[]')
        taxes = request.POST.getlist('tax[]')
        payment_status = request.POST.get('payment_status')
        payment_method = request.POST.get("payment_method")
        customer_email = request.POST.get("customer_email_field")

        if not invoice or not customer_name:
            messages.error(request, 'Invoice number  and Customer Name are required.')
            return redirect('create_invoice')
        
        if not  customer_email:
            messages.error(request, 'Customer Email is required.')
            return redirect('create_invoice')

        for i in range(len(service_names)):
            InvoiceItem.objects.create(
                invoice=invoice,
                payment_status=payment_status,
                payment_method=payment_method,
                customer_name=customer_name, 
                service_name=service_names[i],
                description=descriptions[i],
                quantity=int(quantities[i]),
                price_per_unit=float(prices[i]),
                taxes=float(taxes[i])
            )

        messages.success(request, 'Invoice successfully created.')
        invoice = generate_invoice_number()
        return render(request,'invoice.html',{"invoice":invoice})
    
    invoice = generate_invoice_number()
    return render(request,'invoice.html',{"invoice":invoice})
