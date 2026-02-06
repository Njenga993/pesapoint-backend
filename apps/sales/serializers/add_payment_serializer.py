from rest_framework import serializers

class AddPaymentSerializer(serializers.Serializer):
    method = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_method(self, value):
        """
        Validate that the payment method is one of the allowed choices.
        """
        allowed_methods = ['cash', 'card', 'mpesa']
        if value not in allowed_methods:
            raise serializers.ValidationError(f"Invalid payment method. Allowed methods are: {', '.join(allowed_methods)}")
        return value