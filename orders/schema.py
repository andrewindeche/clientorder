import graphene
from graphene_django.types import DjangoObjectType
from .models import Order, Customer

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "item", "amount")

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "user", "code", "phone")

class Query(graphene.ObjectType):
    customer = graphene.Field(CustomerType)

    order = graphene.Field(OrderType, order_id=graphene.Int(required=True))

    def resolve_customer(self, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                return Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                return None
        return None

    def resolve_order(self, info, order_id):
        return Order.objects.get(id=order_id)

class Mutation(graphene.ObjectType):
    # Mutation to create an order
    create_order = graphene.Field(OrderType, customer_code=graphene.String(), item=graphene.String(), amount=graphene.Float())

    def resolve_create_order(self, info, customer_code, item, amount):
        customer = Customer.objects.get(code=customer_code)
        order = Order.objects.create(customer=customer, item=item, amount=amount)
        return order

schema = graphene.Schema(query=Query, mutation=Mutation)
