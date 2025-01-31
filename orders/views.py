import uuid
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, Customer
from .utils import send_sms_alert
from django.urls import reverse
from . import views

# Create your views here.
def redirect_to_google_login(request):
    return redirect(reverse('socialaccount_login', kwargs={'provider': 'google'}))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    customer_code = request.data.get('customer_code')
    customer = get_object_or_404(Customer, code=customer_code)
    item = request.data.get('item')
    amount = request.data.get('amount')
    
    if not item or not amount:
        return JsonResponse({'error': 'Item and amount are required fields'}, status=400)

    order = Order.objects.create(customer=customer, item=item, amount=amount)

    sms_response = send_sms_alert(customer, order, 'created')

    if isinstance(sms_response, dict) and 'error' in sms_response:
        return JsonResponse({
            'message': 'Order created successfully, but SMS failed.',
            'sms_error': sms_response['error']
        })

    sms_message = sms_response.get('SMSMessageData', {}).get('Message', 'No SMS response')
    sms_status = sms_response.get('SMSMessageData', {}).get('Recipients', [{}])[0].get('status', 'No status')

    return JsonResponse({
        'message': 'Order created successfully',
        'sms_message': sms_message,
        'sms_status': sms_status,
    })

@permission_classes([IsAuthenticated])
class UpdateOrderView(APIView):
    def put(self, request, order_id):
        order = get_object_or_404(Order, order_id=order_id)

        order.item = request.data.get('item', order.item)
        order.amount = request.data.get('amount', order.amount)
        order.save()

        return Response({'message': 'Order updated successfully'}, status=200)

@login_required
def view_customer_code(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
        return JsonResponse({'customer_code': customer.code})
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer does not exist'}, status=404)
    
@login_required
def account_page(request):
    customer = Customer.objects.get(user=request.user)
    phone_updated = False
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone and phone != customer.phone:
            customer.phone = phone
            customer.save()
            phone_updated = True
            return redirect('account_page')

    context = {
        'customer_code': customer.code,
        'customer': customer,
        'phone_updated': phone_updated,
    }
    return render(request, 'accounts/account_page.html', context)

@login_required
def update_phone(request):
    customer = request.user.customer
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            customer.phone = phone
            if not customer.code:
                customer.code = 'CUST' + str(uuid.uuid4().int)[:6]
            customer.save()
            return render(request, 'accounts/account_page.html', {
                'customer': customer,
                'message': 'Phone number updated successfully.'
            })
    
    return render(request, 'accounts/account_page.html', {'customer': customer})