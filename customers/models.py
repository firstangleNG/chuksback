from django.db import models
from django.contrib.postgres.search import SearchVectorField,SearchVector
from django.contrib.postgres.indexes import GinIndex
import uuid

class Customer(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(unique=False,blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)  # Optional field for company name
    address = models.CharField(max_length=255, blank=True, null=True)  # Customer's address
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)  # Secondary phone number
    fax = models.CharField(max_length=20, blank=True, null=True)  # Fax number
    search_vector = SearchVectorField(null=True, blank=True)

    
    class Meta:
        indexes = [GinIndex(fields=['search_vector'])] 


    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the instance first
        # Update search_vector field using an expression
        Customer.objects.filter(id=self.id).update(
            search_vector=SearchVector('first_name', 'last_name', 'company', 'email')
        )

    def __str__(self):
        return f"{self.first_name}"

