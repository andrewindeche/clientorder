from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError
from orders.models import Customer
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created and not instance.is_superuser and not instance.is_staff:
        if not hasattr(instance, 'customer'):
            Customer.objects.create(
                user=instance,
                name=instance.username, 
                email=instance.email
            )

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    if hasattr(instance, 'customer') and not instance.is_superuser and not instance.is_staff:
        instance.customer.save()

@receiver(post_save, sender=User)
def create_or_update_customer(sender, instance, created, **kwargs):
    if not instance.is_staff and not instance.is_superuser:
        try:
            customer, created = Customer.objects.get_or_create(
                user=instance, defaults={'code': 'CUST216204', 'phone': '+2547942346284'}
            )
            if not created:
                # Update the existing customer
                customer.code = 'CUST216204'
                customer.phone = '+2547942346284'
                customer.save()
        except IntegrityError:
            print("An error occurred while creating or updating the customer.")
    else:
        print("User is an admin and cannot be converted to a customer.")