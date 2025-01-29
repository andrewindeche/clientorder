import graphene
from graphene_django.types import DjangoObjectType
from orders.models import Order, Customer

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    all_customers = graphene.List(CustomerType)

    def resolve_all_orders(root, info):
        return Order.objects.all()

    def resolve_all_customers(root, info):
        return Customer.objects.all()

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_code = graphene.String(required=True)
        item = graphene.String(required=True)
        amount = graphene.Decimal(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_code, item, amount):
        customer = Customer.objects.get(code=customer_code)
        order = Order.objects.create(customer=customer, item=item, amount=amount)
        return CreateOrder(order=order)

class UpdateOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.UUID(required=True)
        item = graphene.String()
        amount = graphene.Decimal()

    order = graphene.Field(OrderType)

    def mutate(self, info, order_id, item=None, amount=None):
        order = Order.objects.get(order_id=order_id)
        if item:
            order.item = item
        if amount:
            order.amount = amount
        order.save()
      
schema = graphene.Schema(query=Query)