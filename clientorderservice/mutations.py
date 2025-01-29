import graphene
from orders.models import Order, Customer
import requests
from django.conf import settings
from .types import OrderType

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

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_code = graphene.String(required=True)
        item = graphene.String(required=True)
        amount = graphene.Decimal(required=True)

    order = graphene.Field(lambda: OrderType)

    def mutate(self, info, customer_code, item, amount):
        customer = Customer.objects.get(code=customer_code)
        order = Order.objects.create(customer=customer, item=item, amount=amount)
        return CreateOrder(order=order)

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
