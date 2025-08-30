from rest_framework import serializers
from .models import InvoiceItem

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id','invoice','payment_method','total','customer_name','service_name', 'description', 'quantity', 'price_per_unit', 'taxes']
        read_only_fields = ['total']  # Total will be calculated on save


from .models import Settings
class SettingsSerializer(serializers.ModelSerializer):
    model= Settings
    fields = ["company_email","disclaimer","terms_and_condition",'bank_details']




from rest_framework import serializers
from .models import InvoiceItem

class SingleInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['service_name', 'description', 'quantity', 'price_per_unit', 'taxes', 'total']
