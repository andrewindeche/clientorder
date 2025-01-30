import os
import graphene
from orders.models import Order, Customer
import requests
from graphene_django import DjangoObjectType
from django.conf import settings
from graphql_jwt.decorators import login_required
from django.shortcuts import get_object_or_404
from .types import OrderType
from orders.utils import send_sms_alert 
import africastalking

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

def send_sms_alert(customer, order, action):
    message = f"Dear {customer.name}, your order for {order.item} has been {action}."
    recipients = [customer.phone]
    sms.send(message, recipients)

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class CreateOrderInput(graphene.InputObjectType):
    customer_code = graphene.String(required=True)
    item = graphene.String(required=True)
    amount = graphene.Float(required=True)

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = CreateOrderInput(required=True)
    
    order = graphene.Field(OrderType)
    message = graphene.String()

    @login_required 
    def mutate(self, info, input):
        user = info.context.user 
        customer_code = input.customer_code
        customer = get_object_or_404(Customer, code=customer_code)
        item = input.item
        amount = input.amount

        if not item or not amount:
            return CreateOrder(order=None, message='Item and amount are required fields')

        order = Order.objects.create(customer=customer, item=item, amount=amount)
        send_sms_alert(customer, order, 'created')

        return CreateOrder(order=order, message='Order created successfully')

class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    
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

