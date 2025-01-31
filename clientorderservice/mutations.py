import os
import graphene
import requests
from orders.models import Order, Customer 
from django.conf import settings
from graphql_jwt.decorators import login_required
from django.shortcuts import get_object_or_404
from orders.utils import send_sms_alert 
from decimal import Decimal
import africastalking
from clientorderservice.types import OrderType 

# Initialize Africa's Talking
africastalking.initialize(username=os.getenv('AFRICASTALKING_USERNAME'), 
api_key=os.getenv('AFRICASTALKING_API_KEY'))
sms = africastalking.SMS

class GenerateToken(graphene.Mutation):
    access = graphene.String()
    refresh = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        url = f'{settings.BASE_URL}/api/token/'
        response = requests.post(url, data={"username": username, "password": password})

        if response.status_code == 200:
            token_data = response.json()
            return GenerateToken(
                access=token_data.get('access'),
                refresh=token_data.get('refresh')
            )
        else:
            raise Exception("Invalid credentials")

class RefreshToken(graphene.Mutation):
    access = graphene.String()

    class Arguments:
        refresh = graphene.String(required=True)

    def mutate(self, info, refresh):
        url = f'{settings.BASE_URL}/api/token/refresh/'
        response = requests.post(url, data={"refresh": refresh})

        if response.status_code == 200:
            token_data = response.json()
            return RefreshToken(access=token_data.get('access'))
        else:
            raise Exception("Invalid refresh token")

class CreateOrderInput(graphene.InputObjectType):
    customer_code = graphene.String(required=True)
    item = graphene.String(required=True)
    amount = graphene.Float(required=True)

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = CreateOrderInput(required=True)
    
    order = graphene.Field(OrderType)
    message = graphene.String()
    sms_message = graphene.String()
    sms_status = graphene.String()

    @login_required 
    def mutate(self, info, input):
        user = info.context.user 
        customer_code = input.customer_code
        customer = get_object_or_404(Customer, code=customer_code)
        item = input.item
        amount = Decimal(input.amount) 

        if not item or not amount:
            return CreateOrder(order=None, message='Item and amount are required fields')

        order = Order.objects.create(customer=customer, item=item, amount=amount)
        sms_response = send_sms_alert(customer, order, 'created')

        if sms_response is not None:
            sms_message = sms_response.get('SMSMessageData', {}).get('Message', 'No SMS response')
            sms_status = sms_response.get('SMSMessageData', {}).get('Recipients', [{}])[0].get('status', 'No status')
        else:
            sms_message = 'No SMS response'
            sms_status = 'No status'

        return CreateOrder(
            order=order,
            message='Order created successfully',
            sms_message=sms_message,
            sms_status=sms_status
        )

class UpdateOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.UUID(required=True)
        item = graphene.String()
        amount = graphene.Decimal()

    order = graphene.Field(lambda: OrderType)

    def mutate(self, info, order_id, item=None, amount=None):
        order = Order.objects.get(order_id=order_id)
        if item:
            order.item = item
        if amount:
            order.amount = amount
        order.save()
        return UpdateOrder(order=order)

class Mutation(graphene.ObjectType):
    generate_token = GenerateToken.Field()
    refresh_token = RefreshToken.Field()
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
