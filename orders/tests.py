from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, Order
import uuid
from unittest.mock import patch
from django.middleware.csrf import get_token
from django.test import override_settings

class AccountTests(TestCase):

    def setUp(self):
        User.objects.all().delete()

        self.client = Client()

    def test_signup(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'newuser',
            'password1': 'MyStrongP@ssw0rd!',
            'password2': 'MyStrongP@ssw0rd!',
            'email': 'newuser@example.com',
        })
        if response.status_code == 200:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signin(self):
        self.user = User.objects.create_user(username='testuser', password='MyStrongP@ssw0rd!')
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'MyStrongP@ssw0rd!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

class OrderTests(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Customer.objects.all().delete()
        self.user = User.objects.create_user(username='testuser', password='MyStrongP@ssw0rd!')
        self.user.backend = 'django.contrib.auth.backends.ModelBackend'
        self.client.login(username='johndoe', password='MyStrongP@ssw0rd!', backend=self.user.backend)
        self.client = Client()

        with patch('django.contrib.auth.authenticate') as mock_authenticate:
            mock_authenticate.return_value = self.user
        
        self.user.backend = 'django.contrib.auth.backends.ModelBackend'
        self.client.login(username='testuser', password='MyStrongP@ssw0rd!', backend=self.user.backend)
        self.customer, _ = Customer.objects.get_or_create(user=self.user, defaults={'code': 'CUST216202'})
    
    @override_settings(MIDDLEWARE=[])
    def test_create_order(self):
        response = self.client.get(reverse('create_order'))
        csrf_token = get_token(response.wsgi_request)

        response = self.client.post(reverse('create_order'), {
            'customer_code': 'CUST216202',
            'item': 'Laptop',
            'amount': '500',
            'csrfmiddlewaretoken': csrf_token
        })
        self.assertEqual(response.status_code, 302)
        
class UpdateOrderTests(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Customer.objects.all().delete()

        self.user = User.objects.create_user(username='johndoe', password='MyStrongP@ssw0rd!')
        self.client = Client()
        with patch('django.contrib.auth.authenticate') as mock_authenticate:
            mock_authenticate.return_value = self.user

            self.user.backend = 'django.contrib.auth.backends.ModelBackend'
            self.client.login(username='johndoe', password='MyStrongP@ssw0rd!', backend=self.user.backend)

        self.customer, _ = Customer.objects.get_or_create(user=self.user, defaults={'code': 'CUST216202', 'phone': '1234567890'})

        self.order = Order.objects.create(order_id=uuid.uuid4(), customer=self.customer, item='Laptop', amount=500)
        
    def test_update_order(self):
        response = self.client.put(reverse('update_order', args=[str(self.order.order_id)]), {
            'item': 'Tablet',
            'amount': '400'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.item, 'Tablet')
        self.assertEqual(self.order.amount, 400)


class UpdatePhoneTests(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Customer.objects.all().delete()

        self.user = User.objects.create_user(username='testuser', password='MyStrongP@ssw0rd!')
        self.customer = Customer.objects.create(user=self.user, code='CUST216202', phone='1234567890')
        self.client = Client()
        self.client.login(username='testuser', password='MyStrongP@ssw0rd!')

    def test_update_phone(self):
        response = self.client.post(reverse('update_phone'), {
            'phone': '0987654321'
        })
        self.assertRedirects(response, reverse('account_page'))
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, '+254700044545')

    def test_signin_redirect_to_account_page_and_show_customer_code(self):
        self.client.logout()
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'MyStrongP@ssw0rd!'
        })

        self.assertRedirects(response, reverse('account_page'))
        response = self.client.get(reverse('account_page'))
        self.assertContains(response, 'CUST216202')