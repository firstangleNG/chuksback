from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'imei_serial_no', 'brand', 'model', 'more_detail', 'customer']
        extra_kwargs = {
            'imei_serial_no': {'required': False, 'allow_blank': True}
        }





class PropertyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'imei_serial_no', 'brand', 'model', 'more_detail']
        extra_kwargs = {
            'imei_serial_no': {'required': False, 'allow_blank': True}
        }


from .models import RepairTicket  # Import your model

class RepairTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairTicket
        fields = '__all__'  

    def validate(self, data):
        """
        Custom validation to ensure required fields are provided and valid.
        """
        required_fields = ['customer', 'property', 'problem', 'due_date']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field: "This field is required."})

        return data

class RepairTicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairTicket
        fields = ['id','problem','due_date','bin_location']

class RepairTicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairTicket
        fields = ['problem','due_date','bin_location'] 


from .models import Description

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['id', 'ticket_id', 'description']


class RepairTicketNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairTicket
        fields = ['note']


class RepairTicketTechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairTicket
        fields = ['technician']


from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    payment_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Payment
        fields = ['id','ticket', 'payment_type', 'amount', 'payment_date']

    def validate_payment_type(self, value):
        # Ensure the payment type matches your model's defined choices
        if value not in dict(Payment.PAYMENT_METHOD_CHOICES):
            raise serializers.ValidationError("Invalid payment type.")
        return value


