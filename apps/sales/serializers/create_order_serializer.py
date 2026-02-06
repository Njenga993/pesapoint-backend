from rest_framework import serializers
from apps.sales.models import Order, OrderItem
from apps.products.models import Product

# This serializer is for the items within the creation payload
class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        """
        Ensure the product is active and belongs to the current business.
        The 'context' will be passed from the view.
        """
        if not value.is_active:
            raise serializers.ValidationError("This product is not available for sale.")
        if value.business != self.context['request'].business:
            raise serializers.ValidationError("Invalid product for this business.")
        return value


# This is the main serializer for the create-pos-order action
class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True)

    def create(self, validated_data):
        """
        Create the Order and its associated OrderItems in a single transaction.
        """
        request = self.context['request']
        items_data = validated_data.pop('items')

        # 1. Create the Order, linking it to the business from the request
        order = Order.objects.create(business=request.business)

        # 2. Create each OrderItem
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            # Capture the product's price AT THE TIME OF SALE
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
        
        return order