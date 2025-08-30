from django.db import models


class InvoiceItem(models.Model):
    # ticket_id = models.CharField(max_length=50,blank=True,null=True)  # Link to the ticket
    customer_name = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=50,blank=True,null=True)
    invoice = models.CharField(max_length=50,blank=True,null=True) 
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Calculated field (quantity * price + taxes)
    created_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('Cash', 'Cash'),
            ('Credit/Debit Card', 'Credit/Debit Card'),
            ('Paypal', 'PayPal'),
            ('Stripe', 'Stripe'),
            ('Bank Transfer', 'Bank Transfer')
        ],null=True,blank=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('Not Paid', 'Not Paid'),
            ('Paid', 'Paid')
        ],
        default='Not Paid'
    )
    def get_payment_method_display(self):
        return dict(self._meta.get_field('payment_method').choices).get(self.payment_method)
    
    def save(self, *args, **kwargs):
        base_amount = self.quantity * self.price_per_unit  # Base amount before tax

        # Ensure taxes is treated as a decimal fraction (e.g., 10% -> 0.10)
        tax_rate = self.taxes / 100 if self.taxes > 1 else self.taxes
    
        self.tax_amount = base_amount * tax_rate  # Apply tax to base amount
        self.total = base_amount + self.tax_amount  # Calculate total before saving
    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item for Invoice : {self.invoice}: {self.service_name}"





class Settings(models.Model):
    company_email = models.EmailField(max_length=50)
    disclaimer = models.TextField()
    terms_and_condition = models.TextField()
    bank_details = models.CharField(max_length=100) 

    def __str__(self):
        return "Company Account and Settings details"


