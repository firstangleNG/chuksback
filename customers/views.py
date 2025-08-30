from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
import logging
from django.contrib.auth.decorators import login_required


logger = logging.getLogger('django')

# List all customers
@login_required(login_url='/')
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

# Show details of a single customer
@login_required(login_url='/')
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})



@api_view(['POST'])
# @login_required(login_url='/')
def customer_create(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()  # Save and get the customer instance
        return Response(
            {"message": "Customer created successfully", "customer": customer.id},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
@api_view(['GET'])
def search_customers(request):
    """
    Search for customers using full-text search on first_name, last_name, company, and email.
    Example: GET /api/search-customers/?q=john
    """
    query = request.GET.get('q', '')

    if not query:
        return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Perform full-text search
    search_query = SearchQuery(query)
    results = Customer.objects.annotate(
        rank=SearchRank(F('search_vector'), search_query)
    ).filter(search_vector=search_query).order_by('-rank')

    serializer = CustomerSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_customer_details(request, customer_id):
    """Fetch customer details by ID and return serialized data."""
    customer = get_object_or_404(Customer, id=customer_id)
    serializer = CustomerReadUpdateSerializer(customer)
    return Response(data={"customer_info": serializer.data}, status=status.HTTP_200_OK)




from .serializers import CustomerReadUpdateSerializer
@api_view(["PATCH"])
# @login_required(login_url='/') 
def customer_update(request):
    logger.info("Customer update request received.")

    customer_id = request.data.get("id")
    if not customer_id:
        logger.warning("Customer ID not provided in request.")
        return Response(data={"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    customer = get_object_or_404(Customer, id=customer_id)  
    logger.info(f"Updating customer with ID: {customer_id}")

    serializer = CustomerReadUpdateSerializer(customer, data=request.data, partial=True) 

    if serializer.is_valid():
        serializer.save()
        logger.info(f"Customer {customer_id} updated successfully.")
        return Response(data={"customer_info": serializer.data}, status=status.HTTP_200_OK)
    
    logger.warning(f"Validation errors while updating customer {customer_id}: {serializer.errors}")
    return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  


   
       
# Delete a customer
@login_required(login_url='/')
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})
