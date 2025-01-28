from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, Order

# Create your tests here.
class AccountTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        if not Customer.objects.filter(user=self.user).exists():
            self.customer = Customer.objects.create(user=self.user, phone="1234567890")
        else:
            self.customer = Customer.objects.get(user=self.user)

    def test_signup(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signin(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_update_phone_number(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('account_page'), {
            'phone': '9876543210'
        })
        self.assertEqual(response.status_code, 302) 
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, '9876543210')


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        self.customer = Customer.objects.create(user=self.user, code='CUST216202')

    def test_create_order(self):
        response = self.client.post(reverse('create_order'), {
            'customer_code': 'CUST216202',
            'item': 'Laptop',
            'amount': '500'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(customer_code='CUST216202').exists())

    def test_list_orders(self):
        Order.objects.create(customer_code='CUST216202', item='Laptop', amount=500)
        response = self.client.get(reverse('orders_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        
class UpdateOrderTests(TestCase):

    def setUp(self):
        self.order = Order.objects.create(customer_code='CUST216202', item='Laptop', amount=500)

    def test_update_order(self):
        response = self.client.post(reverse('update_order', args=[self.order.id]), {
            'customer_code': 'CUST216203',
            'item': 'Tablet',
            'amount': '400'
        })
        self.order.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.order.customer_code, 'CUST216203')
        self.assertEqual(self.order.item, 'Tablet')
        self.assertEqual(self.order.amount, 400)

    def test_invalid_amount_update(self):
        response = self.client.post(reverse('update_order', args=[self.order.id]), {
            'customer_code': 'CUST216203',
            'item': 'Tablet',
            'amount': 'invalid_amount'
        })
        self.order.refresh_from_db() 
        self.assertEqual(response.status_code, 200) 
        self.assertNotEqual(self.order.amount, 'invalid_amount')
