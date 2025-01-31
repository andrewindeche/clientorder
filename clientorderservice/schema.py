import graphene
from graphql_jwt.decorators import login_required
from clientorderservice.types import OrderType, CustomerType  # Correct import path
from orders.models import Order, Customer
from clientorderservice.mutations import Mutation  # Correct import path

class Query(graphene.ObjectType):
    customer = graphene.Field(CustomerType)
    order = graphene.Field(OrderType, order_id=graphene.Int(required=True))

    @login_required
    def resolve_customer(self, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                return Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                return None
        return None

    @login_required
    def resolve_order(self, info, order_id):
        return Order.objects.get(id=order_id)

schema = graphene.Schema(query=Query, mutation=Mutation)
