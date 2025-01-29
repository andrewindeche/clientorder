import graphene
from graphene_django.types import DjangoObjectType
from orders.models import Order, Customer

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
