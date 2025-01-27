from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from rest_framework import generics
from .models import Order, Customer
from .serializers import OrderSerializer
from .utils import send_sms_alert

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    customer_code = request.data.get('customer_code')
    customer = get_object_or_404(Customer, code=customer_code)
    item = request.data.get('item')
    amount = request.data.get('amount')

    order = Order.objects.create(customer=customer, item=item, amount=amount)

    send_sms_alert(customer, order, 'created')

    return JsonResponse({'message': 'Order created successfully'})

class UpdateOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        order = serializer.save()
        customer = order.customer
        send_sms_alert(customer, order, 'updated')
