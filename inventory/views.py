from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inventory
from django.db import models
from datetime import datetime, timedelta



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import InventorySerializer

from django.contrib.auth.decorators import login_required



@login_required(login_url='/')
@api_view(['POST'])
@login_required(login_url='/')
def save_or_update_inventory(request):
    try:
        print("Incoming data:", request.data)

        # Serialize the incoming data
        serializer = InventorySerializer(data=request.data)

        if serializer.is_valid():
            sku = serializer.validated_data['sku']
            print("Validated SKU:", sku)

            # Update or create inventory item
            item, created = Inventory.objects.update_or_create(
                sku=sku,
                defaults=serializer.validated_data
            )

            print("Item:", item, "Created:", created)

            # Response message
            if created :
                return Response({'message': "New item added successfully!"}, status=status.HTTP_201_CREATED)
            else:
                 return Response({'message': "Item updated successfully!"}, status=status.HTTP_200_OK)
        print("Serializer errors:", serializer.errors)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception occurred:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@login_required(login_url='/')
def inventory(request):
    if request.method == "POST":
        part_name = request.POST.get("part_name")
        sku = request.POST.get("sku")
        barcode = request.POST.get("barcode")
        category = request.POST.get("category")
        supplier_name = request.POST.get("supplier_name")
        cost_price = request.POST.get("cost_price")
        selling_price = request.POST.get("selling_price")
        quantity = request.POST.get("quantity")
        low_stock_threshold = request.POST.get("low_stock_threshold")
        reorder_level = request.POST.get("reorder_level")
        location = request.POST.get("location")
        expiration_date = request.POST.get("expiration_date")

        # Convert numeric values safely
        try:
            quantity = int(quantity)
            low_stock_threshold = int(low_stock_threshold) if low_stock_threshold else 0
            reorder_level = int(reorder_level) if reorder_level else 0
            cost_price = float(cost_price) if cost_price else None
            selling_price = float(selling_price) if selling_price else None
        except ValueError:
            messages.error(request, "Invalid numeric values entered.")
            return redirect("manage_inventory")

        # Check if item with the same SKU exists
        inventory_item, created = Inventory.objects.get_or_create(
            sku=sku,
            defaults={
                "part_name": part_name,
                "barcode": barcode,
                "category": category,
                "supplier_name": supplier_name,
                "cost_price": cost_price,
                "selling_price": selling_price,
                "quantity_available": quantity,
                "low_stock_threshold": low_stock_threshold,
                "reorder_level": reorder_level,
                "location": location,
                "expiration_date": expiration_date
            }
        )

        if not created:
            # Update existing item
            inventory_item.part_name = part_name
            inventory_item.barcode = barcode
            inventory_item.category = category
            inventory_item.supplier_name = supplier_name
            inventory_item.cost_price = cost_price
            inventory_item.selling_price = selling_price
            inventory_item.quantity_available += quantity  # Add new quantity
            inventory_item.low_stock_threshold = low_stock_threshold
            inventory_item.reorder_level = reorder_level
            inventory_item.location = location
            inventory_item.expiration_date = expiration_date
            inventory_item.save()
            messages.success(request, f"Updated inventory for {part_name} (SKU: {sku}).")
        else:
            messages.success(request, f"Added new inventory item: {part_name} (SKU: {sku}).")

        return redirect("manage_inventory")  # Redirect to inventory page

    return render(request, "add_stock.html")


@login_required(login_url='/')
def low_stock_alerts(request):
    # Query items where available quantity is below the low stock threshold
    low_stock_items = Inventory.objects.filter(quantity_available__lt=models.F('low_stock_threshold'))
    
    return render(request, 'low_stock_alerts.html', {'low_stock_items': low_stock_items})
    # return render(request, 'low_stock_alerts.html', {})



from django.http import JsonResponse

@login_required(login_url='/')
def barcode_scanner(request):
    return render(request, 'barcode_scanner.html')

@login_required(login_url='/')
def scan_barcode(request):
    if request.method == "GET":
        barcode = request.GET.get("barcode", "")
        if barcode:
            try:
                item = Inventory.objects.get(barcode=barcode)
                data = {
                    "part_name": item.part_name,
                    "sku": item.sku,
                    "quantity_available": item.quantity_available,
                    "selling_price": float(item.selling_price) if item.selling_price else None,
                    "location": item.location,
                }
                return JsonResponse({"success": True, "data": data})
            except Inventory.DoesNotExist:
                return JsonResponse({"success": False, "message": "Item not found"})
    return JsonResponse({"success": False, "message": "Invalid request"})


@login_required(login_url='/')
def manage_inventory(request):
    inventory = Inventory.objects.all()
    return render(request, 'manage_inventory.html', {'inventory': inventory})

@login_required(login_url='/')
def inventory_listing(request):
    inventory = Inventory.objects.all()
    return render(request, 'inventory_list.html', {'inventory_items': inventory})

@login_required(login_url='/')
def add_item(request):
    if request.method == "POST":
        part_name = request.POST.get('part_name')
        sku = request.POST.get('sku')
        quantity_available = request.POST.get('quantity_available')
        selling_price = request.POST.get('selling_price')
        
        Inventory.objects.create(
            part_name=part_name,
            sku=sku,
            quantity_available=quantity_available,
            selling_price=selling_price
        )
        return redirect('manage_inventory')
    return render(request, 'add_item.html')

@login_required(login_url='/')
def edit_item(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    if request.method == "POST":
        item.part_name = request.POST.get('part_name')
        item.sku = request.POST.get('sku')
        item.quantity_available = request.POST.get('quantity_available')
        item.selling_price = request.POST.get('selling_price')
        item.save()
        return redirect('manage_inventory')
    return render(request, 'edit_item.html', {'item': item})

@login_required(login_url='/')
def delete_item(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect('manage_inventory')
    return render(request, 'delete_item.html', {'item': item})


@login_required(login_url='/')
def expiring_items(request):
    # Define the threshold (e.g., items expiring within 7 days)
    today = datetime.today().date()
    threshold_date = today + timedelta(days=7)

    # Fetch items that are expiring soon
    expiring_items = Inventory.objects.filter(expiration_date__lte=threshold_date, expiration_date__gte=today)

    return render(request, 'expiring_items.html', {'expiring_items': expiring_items})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Supplier


@login_required(login_url='/')
def supplier_list(request):
    """Display all suppliers."""
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers.html', {'suppliers': suppliers})

@login_required(login_url='/')
def add_supplier(request):
    """Handle supplier creation using raw HTML form."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        if not name:
            messages.error(request, "Supplier name is required.")
        else:
            Supplier.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address
            )
            messages.success(request, "Supplier added successfully.")
            return redirect('supplier_list')

    return render(request, 'supplier_form.html')

@login_required(login_url='/')
def edit_supplier(request, supplier_id):
    """Handle supplier editing using raw HTML form."""
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == "POST":
        supplier.name = request.POST.get("name", supplier.name)
        supplier.email = request.POST.get("email", supplier.email)
        supplier.phone = request.POST.get("phone", supplier.phone)
        supplier.address = request.POST.get("address", supplier.address)
        supplier.save()
        messages.success(request, "Supplier updated successfully.")
        return redirect('supplier_list')

    return render(request, 'supplier_form.html', {'supplier': supplier})


@login_required(login_url='/')
def delete_supplier(request, supplier_id):
    """Handle supplier deletion."""
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == "POST":
        supplier.delete()
        messages.success(request, "Supplier deleted successfully.")
        return redirect('supplier_list')

    return render(request, 'supplier_confirm_delete.html', {'supplier': supplier})



from django.shortcuts import render
from .models import Inventory, SalesTransaction
from django.utils import timezone

@login_required(login_url='/')
def inventory_reports(request):
    total_items = Inventory.objects.count()
    low_stock_count = Inventory.objects.filter(quantity_available__lte=models.F('low_stock_threshold')).count()
    out_of_stock_count = Inventory.objects.filter(quantity_available=0).count()
    expiring_soon_count = Inventory.objects.filter(expiration_date__lte=timezone.now() + timezone.timedelta(days=30)).count()

    recent_updates = Inventory.objects.order_by('-updated_at')[:5]
    total_sales = SalesTransaction.objects.count()
    total_revenue = SalesTransaction.objects.aggregate(total=models.Sum('total_price'))['total'] or 0

    context = {
        "total_items": total_items,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "expiring_soon_count": expiring_soon_count,
        "recent_updates": recent_updates,
        "total_sales": total_sales,
        "total_revenue": total_revenue
    }
    
    return render(request, "reports.html", context)




from django.db.models import Sum
from .models import SalesTransaction


@login_required(login_url='/')
def sales_transactions(request):
    """Displays the sales history and total revenue"""
    sales = SalesTransaction.objects.order_by('-transaction_date')
    total_sales = sales.count()
    total_revenue = sales.aggregate(total=Sum('total_price'))['total'] or 0

    context = {
        "sales": sales,
        "total_sales": total_sales,
        "total_revenue": total_revenue,
    }
    return render(request, "sales_transactions.html", context)


@login_required(login_url='/')
def add_sale(request):
    """Handles adding a new sales transaction"""
    if request.method == "POST":
        item_id = request.POST.get("item")
        quantity_sold = int(request.POST.get("quantity"))

        item = Inventory.objects.get(id=item_id)
        total_price = item.selling_price * quantity_sold

        try:
            sale = SalesTransaction(item=item, quantity_sold=quantity_sold, total_price=total_price)
            sale.save()
            return redirect('sales_transactions')
        except ValueError as e:
            return render(request, "add_sale.html", {"items": Inventory.objects.filter(quantity_available__gt=0), "error": str(e)})

    items = Inventory.objects.filter(quantity_available__gt=0)
    return render(request, "add_sale.html", {"items": items})
