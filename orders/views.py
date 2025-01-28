from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
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

@login_required
def view_customer_code(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
        return JsonResponse({'customer_code': customer.code})
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer does not exist'}, status=404)

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account_page') 
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})


    
@login_required
def account_page(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
        customer_code = customer.code
    except Customer.DoesNotExist:
        customer_code = None 

    context = {
        'customer_code': customer_code,
    }
    return render(request, 'accounts/account_page.html', context)

