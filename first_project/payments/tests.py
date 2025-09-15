from django.test import TestCase, Client
from .models import PaymentCategory, Payment, Person, BankAccount


class PaymentTests(TestCase):
    def setUp(self):
        self.category = PaymentCategory.objects.create(name='Test Category')
        self.person = Person.objects.create(name='John Doe', national_id='123456')
        self.bank_account = BankAccount.objects.create(name='Test Bank', bank_number='123456789')
        self.payment = Payment.objects.create(
            name='Test Payment',
            amount=100.00,
            related_person=self.person,
            payment_method='cash',
            status='pending',
            category=self.category,
            payment_type='out',
            related_bank_account=self.bank_account
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.name, 'Test Payment')
        self.assertEqual(self.payment.category.name, 'Test Category')
        self.assertEqual(self.payment.related_person.name, 'John Doe')
        self.assertEqual(self.payment.related_bank_account.name, 'Test Bank')

    def test_filter_payments_view(self):
        client = Client()
        response = client.get('/filter-payments/?category_id=1&status=pending')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Payment')
