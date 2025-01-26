from django.urls import path
from .views import create_order, UpdateOrderView

urlpatterns = [
    path('create_order/', create_order, name='create_order'),
    path('update_order/<int:pk>/', UpdateOrderView.as_view(), name='update_order'),
]
