
from .models import Property,RepairTicket
from .serializers import RepairTicketSerializer
from django.shortcuts import render,redirect
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer
import random
from django.contrib import messages

from users.models import User
from django.contrib.auth.decorators import login_required


logger = logging.getLogger('django')

import random
from repairs.models import RepairTicket


# def generate_ticket(length=4):
#     while True:
#         # Generate a random 4-digit ticket number
#         ticket = ''.join(random.choices('0123456789', k=length))
        
#         # Check if the ticket already exists in the database
#         used_ticket = RepairTicket.objects.filter(ticket_id=ticket).first()
        
#         if not used_ticket:  # If the ticket is unique, return it
#             return ticket
        


from .models import RepairTicket
# @login_required(login_url='/')
def generate_ticket():
    # Get the latest invoice and increment by 1
    last_ticket = RepairTicket.objects.order_by('-ticket_id').first()

    # Ensure the invoice exists and is a valid numeric string
    if last_ticket and last_ticket.ticket_id and last_ticket.ticket_id.isdigit():
        new_number = int(last_ticket.ticket_id) + 1
    else:
        new_number = 1

    # Return a 6-digit invoice number (e.g., 000001)
    return f"{new_number:06}"



# @login_required(login_url='/')
def add_ticket(request):
    properties = Property.objects.all()  # Retrieve all properties
    ticket = generate_ticket()
    problems = RepairTicket.objects.values_list('problem', flat=True)
    return render(request,"ticket_add.html", {'properties': properties,'ticket':ticket,"problems":problems})

@api_view(["GET"])
# @login_required(login_url='/')
def getAllPropertyData(request):
    properties = Property.objects.all() 
    return Response(data={"properties":properties},status=status.HTTP_200_OK)

# from .models import Description
# # @login_required(login_url='/')
# def ticket_summary(request, id, tk):
#     customer = get_object_or_404(Customer, id=id)
#     ticket = get_object_or_404(RepairTicket, ticket_id=tk)
#     salesman = ticket.salesman.full_name
#     property = ticket.property
#     technicians = User.objects.filter(role="technician").all()

#     descriptions = Description.objects.filter(ticket_id=tk)
    
#     return render(request, "ticket_summary.html", {'customer': customer, "property": property, "ticket": ticket,"salesman":salesman,"technicians":technicians,"descriptions":descriptions})



from .models import Description
from django.shortcuts import get_object_or_404, render
from django.http import Http404

def ticket_summary(request, id, tk):
    try:
        customer = get_object_or_404(Customer, id=id)
        logger.info(f"Fetched customer: ID={id}")
    except Http404:
        logger.error(f"Customer not found: ID={id}")
        raise

    try:
        ticket = get_object_or_404(RepairTicket, ticket_id=tk)
        logger.info(f"Fetched ticket: Ticket ID={tk}")
    except Http404:
        logger.error(f"Ticket not found: Ticket ID={tk}")
        raise

    salesman = ticket.salesman.full_name
    property = ticket.property
    technicians = User.objects.filter(role="technician").all()
    descriptions = Description.objects.filter(ticket_id=tk)

    return render(request, "ticket_summary.html", {
        'customer': customer,
        'address':customer.address,
        'created_at':ticket.created_at,
        "property": property,
        "ticket": ticket,
        "salesman": salesman,
        "technicians": technicians,
        "descriptions": descriptions,
        'status':ticket.status
    })


@api_view(["PATCH"])
# @login_required(login_url='/')
def update_ticket_status(request, ticket_id):
    try:
        # Get the ticket or return 404 if not found
        ticket = RepairTicket.objects.get(ticket_id=ticket_id)
    except RepairTicket.DoesNotExist:
        logger.warning(f"Ticket with ID {ticket_id} not found.")
        return Response({"success": False, "message": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    # Get the new status from the request body
    new_status = request.data.get("status")
    if not new_status:
        return Response({"success": False, "message": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate and update the ticket status
    ticket.status = new_status
    ticket.save()

    return Response({
        "success": True,
        "message": f"Status updated to '{new_status}' successfully.",
        "data": {"ticket_id": ticket.ticket_id, "status": ticket.status}
    }, status=status.HTTP_200_OK)


from .serializers import RepairTicketTechnicianSerializer
@api_view(['POST'])
# @login_required(login_url='/')
def set_technician(request):
    try:
        ticket_id = request.data.get('ticket_id')
        technician_id = request.data.get('technician_id')
        
        logger.info(f"Received request to update technician: ticket_id={ticket_id}, technician_id={technician_id}")

        # Validate the ticket
        try:
            repair_ticket = RepairTicket.objects.get(ticket_id=ticket_id)
            logger.info(f"Repair ticket found: {repair_ticket}")
        except RepairTicket.DoesNotExist:
            logger.warning(f"Repair ticket not found: ticket_id={ticket_id}")
            return Response({'error': 'Repair ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Validate the technician
        try:
            technician = User.objects.get(id=technician_id)
            logger.info(f"Technician found: {technician}")
        except User.DoesNotExist:
            logger.warning(f"Technician not found: technician_id={technician_id}")
            return Response({'error': 'Technician not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the technician
        repair_ticket.technician = technician
        repair_ticket.status = 'Assigned'  # Optionally update the status
        repair_ticket.save()

        logger.info(f"Technician updated successfully for ticket_id={ticket_id} with technician_id={technician_id}")

        serializer = RepairTicketTechnicianSerializer(repair_ticket)
        return Response({'message': 'Technician updated successfully.', 'ticket': serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error updating technician: {str(e)}", exc_info=True)
        return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @login_required(login_url='/')
def property_list(request):
    properties = Property.objects.all()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


from customers.models import Customer
@api_view(['POST'])
# @login_required(login_url='/')
def property_create(request):
    logger.info(f"Incoming Data: {request.data}")  

    customer_id = request.data.get('customer')

    # Validate customer_id before converting to int
    if not customer_id or not str(customer_id).isdigit():
        logger.error(f"Invalid customer ID received: {customer_id}")
        return Response(data={"error": "Invalid customer ID"}, status=status.HTTP_400_BAD_REQUEST)

    customer = Customer.objects.filter(id=int(customer_id)).first()
    if customer is None:
        logger.error(f"Customer not found with ID: {customer_id}")
        return Response(data={"error": "Invalid customer ID"}, status=status.HTTP_400_BAD_REQUEST)

    # Copy request data before modifying
    request_data = request.data.copy()
    request_data['customer'] = customer.pk

    serializer = PropertySerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        return Response(data={"success": "Property creation successful","property":serializer.data}, status=status.HTTP_201_CREATED)

    logger.error(f"Serializer Errors: {serializer.errors}")  # Log validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @login_required(login_url='/')
def property_detail(request, pk):
    try:
        property_obj = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PropertySerializer(property_obj)
    return Response(serializer.data)



from .serializers import PropertyUpdateSerializer
@api_view(['PATCH'])
def property_update(request, pk):
    
    try:
        property_obj = Property.objects.get(pk=pk)
        logger.info(f"Updating Property with ID: {pk}")
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PropertyUpdateSerializer(property_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Property {pk} updated successfully.")
        return Response(serializer.data)
    logger.warning(f"Validation errors while updating property {pk}: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers import RepairTicketDetailSerializer
@api_view(['GET'])
def ticket_detail(request, ticket_id):
    logger.info(f"Received request to fetch details for ticket ID: {ticket_id}")
    
    try:
        ticket_obj = RepairTicket.objects.get(ticket_id=ticket_id)
        logger.error(f"Ticket {ticket_id} found successfully.")
    except RepairTicket.DoesNotExist:
        logger.error(f"Ticket with ID {ticket_id} not found.")
        return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = RepairTicketDetailSerializer(ticket_obj)
    logger.info(f"Returning details for ticket ID: {ticket_id}")
    
    return Response(serializer.data)




from .serializers import RepairTicketUpdateSerializer
@api_view(['PATCH'])
def ticket_update(request, ticket_id):
    try:
        ticket_obj = RepairTicket.objects.get(ticket_id=ticket_id)
        logger.info(f"Updating Repairticket  with ID: {ticket_id}")
    except RepairTicket.DoesNotExist:
        logger.error(f"Ticket does not exist: {ticket_id}")
        return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = RepairTicketUpdateSerializer(ticket_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Ticket  {ticket_id} updated successfully.")
        return Response(serializer.data)
    logger.warning(f"Validation errors while updating Repair Ticket {ticket_id}: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
# @login_required(login_url='/')
def property_delete(request, pk):
    try:
        property_obj = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

    property_obj.delete()
    return Response({"message": "Property deleted successfully"}, status=status.HTTP_204_NO_CONTENT)









from django.shortcuts import get_object_or_404
@api_view(['POST'])
# @login_required(login_url='/')
def create_repair_ticket(request):
    logger.info("Incoming Data: %s", request.data)

    # Get and validate USer, customer & property IDs
    salesman_id = request.data.get('salesman')
    customer_id = request.data.get('customer')
    property_id = request.data.get('property')
   

    if not salesman_id:
        logger.error("Missing required fields. Salesman ID.")
        return Response({"error": "Salesman ID are required."}, status=status.HTTP_400_BAD_REQUEST)

    if not customer_id or not property_id:
        logger.error("Missing required fields: customer or property ID.")
        return Response({"error": "Customer ID and Property ID are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        customer_id = int(customer_id)
        property_id = int(property_id)
    except ValueError:
        logger.error("Invalid ID format: Customer ID or Property ID must be an integer.")
        return Response({"error": "Customer ID and Property ID must be integers."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate salesman,customer and property using `get_object_or_404`
    salesman = get_object_or_404(User, id=salesman_id)
    customer = get_object_or_404(Customer, id=customer_id)
    property_obj = get_object_or_404(Property, id=property_id)

    # Prepare data for serializer
    request_data = request.data.copy()
    request_data['salesman'] = salesman.pk
    # request_data['technician'] = salesman.full_name
    request_data['customer'] = customer.pk
    request_data['property'] = property_obj.pk

    serializer = RepairTicketSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        logger.info("Repair ticket created successfully for customer ID %d, property ID %d.", customer_id, property_id)
        return Response({"success": "Repair ticket created successfully!"}, status=status.HTTP_201_CREATED)

    logger.error("Validation errors: %s", serializer.errors)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




from django.shortcuts import render
# @login_required(login_url='/')
def ticket_list(request,user_id):
    # Load all repair tickets with related customer, property, technician, and salesman
    tickets = RepairTicket.objects.select_related(
        'customer', 'property', 'technician', 'salesman'
    ).order_by('-created_at')

    
    technicians = User.objects.all()

      # Ensure user exists or return 404 if not found
    logged_in_user = get_object_or_404(User, id=user_id)
    # Include all status choices from the model
    status_choices = RepairTicket.STATUS_CHOICES

    context = {
        'tickets': tickets,
        'technicians': technicians,
        'STATUS_CHOICES': status_choices,
        'logged_in_user': logged_in_user, 
    }
    return render(request, 'ticket.html', context)



from django.db import IntegrityError
from .serializers import DescriptionSerializer
@api_view(['POST'])
# @login_required(login_url='/')
def add_description(request):
    try:
        ticket_id = request.data.get('ticket_id')
        description = request.data.get('description')  

        if not (description and ticket_id):
            message = "Ticket, and Description are required."
            logger.error(f"Validation error: {message}")
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        ticket_id = RepairTicket.objects.get(ticket_id=ticket_id)
    except (RepairTicket.DoesNotExist) as e:
        message = f"Invalid Ticket ID.({ticket_id})"
        logger.error(f"Validation error: {message} - {e}")
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Validate and save description
        serializer = DescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Description added successfully!", "description": serializer.data}, status=status.HTTP_201_CREATED)

        message = "Invalid data in description serializer."
        logger.error(f"Serializer error: {message} - {serializer.errors}")
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except IntegrityError as e:
        message = "Duplicate entry or data conflict."
        logger.error(f"IntegrityError: {message} - {e}")
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        message = "An unexpected error occurred."
        logger.error(f"Unexpected error: {message} - {e}")
        return Response({"message": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


from invoice.views import getAllTotals
from .tasks import send_email_ticket
from babel.numbers import format_currency
from datetime import datetime
@api_view(["POST"])
def email_tickets(request):
    customer_id = request.data.get("customer_id")
    ticket_id = request.data.get("ticket_id")
    email = request.data.get("email")

  
    if not all([customer_id,ticket_id,email]):
        logger.error(f"Error occurred: Either customer id , ticket id or email is not found in request data")
        return Response({"error": "Either customer id , ticket id or email is not found in request data"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate customer and ticket
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        logger.error(f"Error occurred: Invalid customer ID {customer_id}")
        return Response({"error": "Invalid customer ID"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ticket = RepairTicket.objects.get(ticket_id=ticket_id)
    except RepairTicket.DoesNotExist:
        logger.error(f"Error occurred: Invalid ticket ID {ticket_id}")
        return Response({"error": "Invalid ticket ID"}, status=status.HTTP_400_BAD_REQUEST)
    
     # Get all invoice items for the particular invoice number linked to the ticket
    invoice_items = InvoiceItem.objects.filter(invoice=ticket.invoice)
    tax_statement = ""
    tax_count = len([item for item in invoice_items if item.taxes > 0])
    tax_statement = f"( 20% tax inclusive on {tax_count} items )" if tax_count > 0 else  f"( 0% tax inclusive )"

    if invoice_items:
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
            grand_total,total_tax = getAllTotals(invoice=ticket.invoice)
            total_paid = getTotalPaidAmountForTicket(ticket=ticket_id)
            gbp_formatted_grand_total = format_currency(grand_total, 'GBP', locale='en_GB')
            gbp_formatted_total_tax = format_currency(total_tax, 'GBP', locale='en_GB')
            gbp_formatted_subtotal = format_currency(Decimal(grand_total) - Decimal(total_tax)
        , 'GBP', locale='en_GB') 
            gbp_formatted_total_paid= format_currency(total_paid
        , 'GBP', locale='en_GB') 
        
            gbp_formatted_amount_due = format_currency(Decimal(grand_total) - Decimal(total_paid)
        , 'GBP', locale='en_GB') 
            

    else:
        # No invoice items found
        logger.warning(f"Warning: No invoice items found for ticket ID {ticket_id}")
        items_list = []  # Empty list if no items
        # Default values for payment details
        gbp_formatted_grand_total = format_currency(0, 'GBP', locale='en_GB')
        gbp_formatted_total_tax = format_currency(0, 'GBP', locale='en_GB')
        gbp_formatted_subtotal = format_currency(0, 'GBP', locale='en_GB')
        gbp_formatted_total_paid = format_currency(0, 'GBP', locale='en_GB')
        gbp_formatted_amount_due = format_currency(0, 'GBP', locale='en_GB') 

        

    descriptions = Description.objects.filter(ticket_id=ticket_id) 
    description_list = []
    if descriptions:
        for description in descriptions:
            description_list.append({
                "created_at": description.created_at.isoformat(),
                "description": description.description
            })
    else:
        description_list = []

    try:
        device = ticket.property 

        scheme = request.scheme
        host = request.get_host()
        endpoint = f"{scheme}://{host}"

        # Async email task
        send_email_ticket.delay_on_commit(
            endpoint=endpoint,
            email=email,
            customer={
                "name": f"{customer.first_name} {customer.last_name}",
                "email": email,
                "phone": customer.phone,
                "address":customer.address
            },
            ticket={
                "id": ticket.ticket_id,
                "problem": ticket.problem,
                "due_date": str(ticket.due_date),
                "bin_location": ticket.bin_location,
                "technician": ticket.technician.full_name if ticket.technician else "Not Assigned",
                "salesman": ticket.salesman.full_name if ticket.salesman else "Not Assigned",
                "status": str(ticket.status),
                "creation_date":ticket.created_at,
                "current_date_time": datetime.now()

            },
            device_proper={
                "imei_serial": device.imei_serial_no,
                "brand": device.brand,
                "model": device.model,
                "details": device.more_detail
            },
            payment_details={
                "total_amount":gbp_formatted_subtotal,
                "grand_total": gbp_formatted_grand_total,
                'total_tax':gbp_formatted_total_tax,
                'total_paid': gbp_formatted_total_paid,
                'amount_due': gbp_formatted_amount_due,
                'tax_statement' : tax_statement
            },
           invoices={
                "invoices": items_list   # Pass all invoice items to the email template
            } ,
            descriptions ={
                "descriptions":description_list
            }
                                
        )

        return Response({"message": "Email is being sent"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
# @login_required(login_url='/')
def get_customer_email(request):
    customer_id = request.data.get("customer_id")
    
    if not customer_id:
        logger.error("Error occurred: Customer ID not in request data")
        return Response({"error": "Invalid customer ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    customer = Customer.objects.filter(id=customer_id).first()
    
    if customer is None:
        logger.error(f"Error occurred: Customer with ID {customer_id} not found")
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({"email": customer.email}, status=status.HTTP_200_OK)



from .serializers import RepairTicketNoteSerializer

# Retrieve notes (GET)
@api_view(['GET'])
# @login_required(login_url='/')
def get_repair_ticket_notes(request, ticket_id):
    ticket = get_object_or_404(RepairTicket, ticket_id=ticket_id)
    serializer = RepairTicketNoteSerializer(ticket)
    return Response(serializer.data)

# Create a note 
@api_view(['POST'])
# @login_required(login_url='/')
def create_repair_ticket_note(request, ticket_id):
    ticket = get_object_or_404(RepairTicket, ticket_id=ticket_id)
    serializer = RepairTicketNoteSerializer(ticket, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from .models import Payment
from .serializers import PaymentSerializer
from django.db.models import Sum

def getTotalPaidAmountForTicket(ticket):
    total_amount  = Payment.objects.filter(ticket=ticket).aggregate(total_sum=Sum("amount"))['total_sum']
    return total_amount or 0




@api_view(['GET', 'POST'])
def payment_list_create(request):
    # List all payments
    if request.method == 'GET':
        ticket = request.GET.get('ticket')
        logger.info(f"GET request received for ticket: {ticket}")
        
        # Query payments
        payments = Payment.objects.filter(ticket=ticket)
        serializer = PaymentSerializer(payments, many=True)
        
        # Calculate total paid amount for the ticket
        total_paid_amount = getTotalPaidAmountForTicket(ticket)
        
        # Log total paid amount
        logger.info(f"Total paid amount for ticket {ticket}: {total_paid_amount}")
        
        # Add the total to the response
        return Response({
            'payments': serializer.data,
            'total_paid_amount': total_paid_amount
        })

    # Create a new payment
    elif request.method == 'POST':
        logger.info("POST request received for creating payment.")
        
        # Validate and save the payment
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Payment recorded successfully: {serializer.data}")
            return Response({
                "message": "Payment recorded successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        # Log the validation errors
        logger.error(f"Payment creation failed. Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @login_required(login_url='/')
def delete_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        payment.delete()
        return Response({"message": "Payment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)




from invoice.models import InvoiceItem
from decimal import Decimal
@api_view(["GET"])
def get_amount_due(request, ticket_id):
    logger.info(f"Received request to count payments for ticket_id: {ticket_id}")

    # Query for all payments with the given ticket_id
    payments = Payment.objects.filter(ticket=ticket_id)
    total_payments = payments.count()

    logger.info(f"Total payments found: {total_payments}")

    # Sum the amounts of all payments
    total_paid_amount = payments.aggregate(total_paid_amount=Sum('amount'))['total_paid_amount'] or 0.00
    logger.info(f"Total paid amount: {total_paid_amount}")

    # Get the associated invoice
    try:
        invoice = get_object_or_404(RepairTicket, ticket_id=ticket_id).invoice
        logger.info(f"Invoice found for ticket_id {ticket_id}: {invoice}")
    except Exception as e:
        logger.error(f"Error retrieving invoice for ticket_id {ticket_id}: {e}")
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

    # Calculate total invoice amount
    total_amount_invoice_amount = InvoiceItem.objects.filter(invoice=invoice).aggregate(
        total_amount_invoice_amount=Sum('total')
    )['total_amount_invoice_amount'] or 0.00

    logger.info(f"Total invoice amount: {total_amount_invoice_amount}")

    # Calculate the amount due
    amount_due = total_amount_invoice_amount - Decimal(total_paid_amount)
    logger.info(f"Amount due: {amount_due}")

    response_data = {
        'ticket_id': ticket_id,
        'total_payments': total_payments,
        'total_paid_amount': total_paid_amount,
        'total_invoice_amount': total_amount_invoice_amount,
        'amount_due': amount_due
    }

    logger.info(f"Response data: {response_data}")

    return Response(response_data, status=status.HTTP_200_OK)



