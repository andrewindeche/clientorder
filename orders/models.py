from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  unique=True, null=True, blank=True) 
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField()
    registration_date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = 'CUST' + str(uuid.uuid4().int)[:6] 
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')
    payment_method = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    order_id = models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    
    def __str__(self):
        return f"Order {self.order_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
