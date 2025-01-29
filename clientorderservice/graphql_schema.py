import graphene
from .types import OrderType, CustomerType
from .mutations import GenerateToken, RefreshToken, CreateOrder, UpdateOrder
from orders.models import Order, Customer

class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    all_customers = graphene.List(CustomerType)

    def resolve_all_orders(root, info):
        return Order.objects.all()

    def resolve_all_customers(root, info):
        return Customer.objects.all()

class Mutation(graphene.ObjectType):
    generate_token = GenerateToken.Field()
    refresh_token = RefreshToken.Field()
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
