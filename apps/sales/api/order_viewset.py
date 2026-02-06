from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.db import transaction

from apps.sales.models import Order, Payment
from apps.sales.serializers import OrderSerializer
from apps.sales.serializers.create_order_serializer import CreateOrderSerializer
from apps.sales.serializers.add_payment_serializer import AddPaymentSerializer
from apps.businesses.api.permissions import IsBusinessManager
from apps.products.models import Inventory, InventoryTransaction

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsBusinessManager]
    queryset = Order.objects.all() # Add this base queryset

    def get_queryset(self):
        return Order.objects.filter(
            business=self.request.business
        ).select_related("business")

    def perform_create(self, serializer):
        serializer.save(business=self.request.business)

    # -------------------------------------------
    # CUSTOM ACTION: CREATE POS ORDER
    # -------------------------------------------
    @action(detail=False, methods=['post'], url_path='create-pos-order')
    def create_pos_order(self, request):
        """
        Creates a new order with items in a single transaction.
        Expected Payload:
        {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 5, "quantity": 1}
            ]
        }
        """
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    # -------------------------------------------
    # CUSTOM ACTION: ADD PAYMENT
    # -------------------------------------------
    @action(detail=True, methods=['post'], url_path='add-payment')
    def add_payment(self, request, pk=None):
        """
        Adds a payment to a specific order, completes the order if fully paid, and decrements inventory.
        The 'pk' in the URL is the Order ID.
        Expected Payload:
        {
            "method": "cash",  // or "mpesa", "card"
            "amount": "25.50"
        }
        """
        order = self.get_object()

        if order.status == Order.STATUS_COMPLETED:
            raise serializers.ValidationError("Cannot add payment to a completed order.")

        serializer = AddPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # 1. Create the payment linked to the order
             payment = Payment.objects.create(
                order=order,
                **serializer.validated_data
            )
            
            # 2. Re-calculate paid amount and update order status
             order_serializer = OrderSerializer(order)
             order_data = order_serializer.data
             total_amount = float(order_data['total_amount'])
             paid_amount = float(order_data['paid_amount']) + float(payment.amount)

             if paid_amount >= total_amount:
                order.payment_status = Order.PAYMENT_PAID
                order.status = Order.STATUS_COMPLETED
                order.save()

                # 3. --- THE CRITICAL PART: DECREMENT INVENTORY ---
                for item in order.items.all():
                    try:
                        inventory = Inventory.objects.select_for_update().get(
                            business=order.business,
                            product=item.product
                        )

                        if inventory.quantity < item.quantity:
                            raise serializers.ValidationError(
                                f"Sale failed! Not enough stock for {item.product.name}. "
                                f"Available: {inventory.quantity}, Needed: {item.quantity}."
                            )
                            

                        inventory.quantity -= item.quantity
                        inventory.save()

                        InventoryTransaction.objects.create(
                            business=order.business,
                            product=item.product,
                            transaction_type=InventoryTransaction.TRANSACTION_OUT,
                            quantity=-item.quantity,
                            note=f"Sale - Order #{order.id}"
                        )

                    except Inventory.DoesNotExist:
                        raise serializers.ValidationError(
                            f"Sale failed! No inventory record found for product {item.product.name}."
                        )
            
            # 4. Return the fully updated order
             return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        
        