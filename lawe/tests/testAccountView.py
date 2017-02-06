''' Тесты для страницы отчета по счету '''
from django.contrib.auth.models import User
from django.test import Client, TestCase
from lawe.models import Account, Transaction


class TestAccountView(TestCase):
	''' Тестирование AccountView '''
	def setUp(self):
		''' Другой аккаунт мы создадим заранее, чтобы он не замусоривал тесты '''
		self.oacc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		self.user = User.objects.create_user('john', 'password')
		self.client = Client()
		self.client.force_login(self.user)

	def testZeroAccount(self):
		''' Аккаунт без транзакций выдает сумму 0 '''
		# Given
		acc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		# When
		response = self.client.get('/account/%u' % acc.id)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn('<total>0</total>', response.content.decode('utf8'))

	def testCreditedAccount(self):
		''' На счет перечислены деньги '''
		# Given
		acc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		Transaction.objects.create(debit=self.oacc, credit=acc, amount=100, description='')
		# When
		response = self.client.get('/account/%u' % acc.id)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn('<total>100</total>', response.content.decode('utf8'))
		self.assertIn('<income>100</income>', response.content.decode('utf8'))

	def testDebitAccount(self):
		''' Со счетасписаны  деньги '''
		# Given
		acc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		Transaction.objects.create(debit=acc, credit=self.oacc, amount=100, description='')
		# When
		response = self.client.get('/account/%u' % acc.id)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn('<total>-100</total>', response.content.decode('utf8'))
		self.assertIn('<outcome>100</outcome>', response.content.decode('utf8'))
