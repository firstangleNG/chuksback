


from django.shortcuts import render
from django.db import models
from invoice.models import InvoiceItem
from repairs.models import RepairTicket
from inventory.models import Inventory
from django.db.models import Sum,F
from django.contrib.auth.decorators import login_required

@login_required(login_url='/') 
def dashboard(request):
    total_revenue = InvoiceItem.objects.filter(payment_status='Paid').aggregate(total=Sum('total'))['total'] or 0
    pending_payments = InvoiceItem.objects.filter(payment_status='Not Paid').aggregate(total=Sum('total'))['total'] or 0
    total_tickets = RepairTicket.objects.count()
    open_tickets = RepairTicket.objects.filter(status__in=['New', 'In Progress','Assigned','Diagnosed','Awaiting Parts','']).count()
    canceled_tickets = RepairTicket.objects.filter(status='Canceled').count()
    completed_tickets = RepairTicket.objects.filter(status='Completed').count()
    closed_tickets = RepairTicket.objects.filter(status='Closed').count()
    low_stock_items = Inventory.objects.filter(quantity_available__lte=F('low_stock_threshold')).count()


    context = {
        'total_revenue': total_revenue,
        'pending_payments': pending_payments,
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'canceled':canceled_tickets,
        'completed':completed_tickets,
        'closed_tickets': closed_tickets,
        'low_stock_items': low_stock_items,
    }
    return render(request, 'dashboard.html', context)
