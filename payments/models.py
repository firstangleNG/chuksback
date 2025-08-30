# from django.db import models

# class Invoice(models.Model):
#     PAYMENT_STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("paid", "Paid"),
#     ]
#     PAYMENT_METHOD_CHOICES = [
#         ("cash", "Cash"),
#         ("card", "Card"),
#         ("transfer","Transfer"),
#         ("paypal", "PayPal"),
#     ]
#     repair_ticket = models.OneToOneField('repairs.RepairTicket', on_delete=models.CASCADE)
#     amount_due = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending")
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
#     paid_at = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
