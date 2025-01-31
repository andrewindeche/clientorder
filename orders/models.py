from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField()
    registration_date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, blank=True, null=True)
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
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        pass

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, to_field='order_id')
    item = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.item} in Order {self.order.order_id}"
