from django.db import IntegrityError
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, Order
import uuid
from django.middleware.csrf import get_token
from unittest.mock import patch

class AccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'newuser1',
            'password1': 'MyStrongP@ssw0rd1!',
            'password2': 'MyStrongP@ssw0rd1!',
            'email': 'newuser1@example.com',
        })
        if response.status_code == 200:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser1').exists())

    def test_signin(self):
        self.user = User.objects.create_user(username='testuser1', password='MyStrongP@ssw0rd1!')
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser1',
            'password': 'MyStrongP@ssw0rd1!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
    def test_view_customer_code_authenticated(self):
        self.user = User.objects.create_user(username='testuser', password='MyStrongP@ssw!')
        self.client.login(username='testuser', password='MyStrongP@ssw!')
        response = self.client.get(reverse('view_customer_code'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'customer_code')

    def test_view_customer_code_unauthenticated(self):
        response = self.client.get(reverse('view_customer_code'))
        self.assertEqual(response.status_code, 302)
        
    def tearDown(self):
        User.objects.all().delete()
        Customer.objects.all().delete()

class OrderTests(APITestCase):

    def setUp(self):
        Order.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()

        self.user = User.objects.create_user(username='testuser2', password='MyStrongP@ssw0rd2!')
        self.customer, created = Customer.objects.get_or_create(user=self.user, defaults={'code': 'CUST216201'})

        self.token, _ = Token.objects.get_or_create(user=self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 200)
        csrf_token = get_token(response.wsgi_request)
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(reverse('create_order'), {
            'customer_code': 'CUST216202',
            'item': 'Laptop',
            'amount': '500',
            'csrfmiddlewaretoken': csrf_token
        }, **headers)
        self.assertEqual(response.status_code, 302)

class UpdateOrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser3', password='MyStrongP@ssw0rd3!')
        self.customer, created = Customer.objects.get_or_create(user=self.user, defaults={'code': 'CUST216203', 'phone': '1234567890'})
        self.order = Order.objects.create(order_id=uuid.uuid4(), customer=self.customer, item='Laptop', amount=500)
        
        self.token, _ = Token.objects.get_or_create(user=self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_order(self):
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.put(reverse('update_order', args=[str(self.order.order_id)]), {
            'item': 'Tablet',
            'amount': '400'
        }, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)

        self.order.refresh_from_db()
        self.assertEqual(self.order.item, 'Tablet')
        self.assertEqual(self.order.amount, 400)

def generate_unique_code():
    return 'CUST' + str(uuid.uuid4()).replace('-', '')[:8]

class UpdatePhoneTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345')
        if not self.user.is_staff and not self.user.is_superuser:
            try:
                code = generate_unique_code()
                self.customer, created = Customer.objects.get_or_create(
                    user=self.user, defaults={'code': code, 'phone': '+2547942346284'}
                )
                if not created:
                    self.customer.code = code
                    self.customer.phone = '+2547942346284'
                    self.customer.save()
            except IntegrityError:
                print("An error occurred while creating or updating the customer.")
        else:
            print("User is an admin and cannot be converted to a customer.")

    def test_update_phone(self):
        response = self.client.post(reverse('update_phone'), {
            'phone': '+254794000000'
        })
        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, '+254794000000')
        
    def tearDown(self):
        User.objects.all().delete()
        Customer.objects.all().delete()
