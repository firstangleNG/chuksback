from django.db import models

class Inventory(models.Model):
    part_name = models.CharField(max_length=255, db_index=True)
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity_available = models.PositiveIntegerField(blank=True, null=True)
    low_stock_threshold = models.PositiveIntegerField(blank=True, null=True)
    reorder_level = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.part_name} (SKU: {self.sku})"



from django.utils import timezone

class SalesTransaction(models.Model):
    item = models.ForeignKey('Inventory', on_delete=models.CASCADE, related_name="sales")
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Ensure the inventory has enough stock before saving the transaction
        if self.item.quantity_available >= self.quantity_sold:
            self.item.quantity_available -= self.quantity_sold
            self.item.save()
        else:
            raise ValueError("Not enough stock available")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity_sold} x {self.item.part_name} on {self.transaction_date}"



class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
