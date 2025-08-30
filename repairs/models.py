from django.db import models
from users.models import User 
from customers.models import Customer


class Property(models.Model):
    imei_serial_no = models.CharField(max_length=50,blank=True,null=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    more_detail = models.CharField(max_length=100,blank=True,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='properties')
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.imei_serial_no})"


class RepairTicket(models.Model):
    # Ticket Information
    ticket_id = models.CharField(max_length=100, unique=True)
    invoice = models.CharField(max_length=100, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='repair_tickets')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='repair_tickets')
    problem = models.TextField()
    due_date = models.CharField(max_length=100)  # Using CharField to include both date and time
    password = models.CharField(max_length=50, blank=True, null=True)
    bin_location = models.CharField(max_length=200, blank=True, null=True)
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_repair_tickets')
    salesman = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sold_repair_tickets')

    # Payment Information
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
 
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Assigned', 'Assigned'),
        ('Diagnosed', 'Diagnosed'),
        ('In Progress', 'In Progress'),
        ('Awaiting Parts', 'Awaiting Parts'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Closed', 'Closed'),
        ('Canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    note = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)


    def calculate_total_price(self):
        # This is an example method to calculate total price if it's based on some factors (e.g., parts or services)
        self.total_price = self.amount_due  
        self.save()
        
    def __str__(self):
        return f"Repair Ticket {self.ticket_id} - {self.customer.first_name}  - {self.problem}"




class Description(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='description')
    ticket_id = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Description for  Ticket : {self.ticket_id}"



class ProductHistory(models.Model):
    ticket = models.ForeignKey(RepairTicket, on_delete=models.CASCADE, related_name='history')
    date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    details = models.TextField()
    
    def __str__(self):
        return f"Activity on {self.date} by {self.user}: {self.activity}"


class Payment(models.Model):
    # Define choices for payment types
    PAYMENT_METHOD_CHOICES = [
        
            ('Cash', 'Cash'),
            ('Credit/Debit Card', 'Credit/Debit Card'),
            ('Paypal', 'PayPal'),
            ('Stripe', 'Stripe'),
            ('Bank Transfer', 'Bank Transfer')
    ]
    
    ticket = models.CharField(max_length=30)
    payment_type = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES,  # Add choices to restrict to predefined payment methods
        default='cash'  # Set a default payment type
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for Ticket {self.ticket}"
    
# PostgreSQL specific model
from django.contrib.postgres.fields import ArrayField

class MyModel(models.Model):
    items = ArrayField(models.CharField(max_length=200), blank=True, default=list)
