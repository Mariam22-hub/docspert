from django.test import TestCase, Client
from django.urls import reverse
from .models import Account
import io
import uuid

class AccountTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.account1 = Account.objects.create(id=uuid.uuid4(), name="Account1", balance=1000)
        self.account2 = Account.objects.create(id=uuid.uuid4(), name="Account2", balance=2000)

    def test_account_creation(self):
        self.assertEqual(self.account1.balance, 1000)
        self.assertEqual(self.account2.balance, 2000)

    def test_import_accounts(self):
        csv_file = io.StringIO("ID,Name,Balance\ncc26b56c-36f6-41f1-b689-d1d5065b95af,Joy Dean,4497.22\nbe6acfdc-cae1-4611-b3b2-dfb5167ba5fe,Bryan Rice,2632.76")
        response = self.client.post(reverse('import_accounts'), {'csv_file': csv_file})
        self.assertEqual(response.status_code, 302)  # Redirect after successful import
        self.assertEqual(Account.objects.count(), 4)
        self.assertTrue(Account.objects.filter(name="Joy Dean").exists())
        self.assertTrue(Account.objects.filter(name="Bryan Rice").exists())

    def test_list_accounts(self):
        response = self.client.get(reverse('list_accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Account1")
        self.assertContains(response, "Account2")

    def test_account_info(self):
        response = self.client.get(reverse('account_info', args=[self.account1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'name': 'Account1', 'balance': '1000.00'}
        )

    def test_transfer_funds(self):
        response = self.client.post(reverse('transfer_funds'), {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': 500
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful transfer
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account1.balance, 500)
        self.assertEqual(self.account2.balance, 2500)

    def test_insufficient_funds_transfer(self):
        response = self.client.post(reverse('transfer_funds'), {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': 1500
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account1.balance, 1000)
        self.assertEqual(self.account2.balance, 2000)
