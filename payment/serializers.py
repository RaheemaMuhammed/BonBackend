from rest_framework import serializers
from .models import PaymentRequest
class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = ['user','upi_id', 'amount']