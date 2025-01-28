from django.urls import path
from . import views
from .views import create_order, UpdateOrderView

urlpatterns = [
    path('create_order/', create_order, name='create_order'),
    path('update_order/<int:pk>/', UpdateOrderView.as_view(), name='update_order'),
    path('account_page/', views.account_page, name='account_page'),
    path('signup/', views.signup_view, name='register'),
    path('update-phone/', views.account_page, name='update_phone'), 
]
