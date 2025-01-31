from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, Order
import uuid
from django.test import TestCase
from django.test import Client

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
        self.user = User.objects.create_user(username='testuser3', password='MyStrongP@ssw0rd3!')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.customer, _ = Customer.objects.get_or_create(
            user=self.user, 
            defaults={'code': 'CUST216204', 'phone': '+25470987654'}
        )
        
        self.order = Order.objects.create(
            order_id=uuid.uuid4(),
            customer=self.customer,
            item='Laptop',
            amount=500
        )

        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_order(self):
        data = {
            'customer_code': 'CUST216204',
            'item': 'Laptop',
            'amount': 500
        }

        response = self.client.post(reverse('create_order'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'Order created successfully')

class UpdateOrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser3', password='MyStrongP@ssw0rd3!')
        self.customer, created = Customer.objects.get_or_create(user=self.user, defaults={'code': 'CUST216203', 'phone': '1234567890'})
        self.order = Order.objects.create(order_id=uuid.uuid4(), customer=self.customer, item='Laptop', amount=500)
        
        self.token, _ = Token.objects.get_or_create(user=self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_order(self):
        order = Order.objects.create(customer=self.customer, item='Old Item', amount=100)
        data = {
            'item': 'New Laptop',
            'amount': 500
        }
        
        order_uuid = order.order_id 
        url = reverse('update_order', kwargs={'order_id': order_uuid})
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.item, 'New Laptop')
        self.assertEqual(order.amount, 500)

def generate_unique_code():
    return 'CUST' + str(uuid.uuid4()).replace('-', '')[:8]

class UpdatePhoneTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer, _ = Customer.objects.get_or_create(
            user=self.user, defaults={'code': 'some_unique_code', 'phone': '+2547942346284'}
        )

    def test_update_phone(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('update_phone'), {
            'phone': '+254794000000'
        })

        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, '+254794000000')
        
    def tearDown(self):
        User.objects.all().delete()
        Customer.objects.all().delete()

class SecurityTests(TestCase):
    def test_password_encryption(self):
        user = User.objects.create_user(username='user', password='password')
        self.assertNotEqual(user.password, 'password') 

    def test_logout(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        
        self.client.logout()
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('account_page'))
        self.assertRedirects(response, reverse('account_login') + '?next=' + reverse('account_page')) 
        
    def test_xss_protection(self):
        malicious_script = "<script>alert('XSS');</script>"
        response = self.client.post(reverse('update_phone'), {'text': malicious_script})
        self.assertNotIn(malicious_script, response.content.decode())

    def test_csrf_protection_with_missing_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'data': 'test'})
        self.assertEqual(response.status_code, 400)