from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    registration_date = models.DateTimeField(auto_now_add=True)
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')
    payment_method = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
