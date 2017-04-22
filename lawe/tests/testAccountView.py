''' Тесты для страницы отчета по счету '''
from xml.etree import ElementTree
from django.contrib.auth.models import User
from django.test import Client, TestCase
from lawe.models import Account, Transaction


class TestAccountView(TestCase):
	''' Тестирование AccountView '''
	def setUp(self):
		self.user = User.objects.create_user('john', 'password')
		# Другой аккаунт мы создадим заранее, чтобы он не замусоривал тесты
		self.oacc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		self.oacc.allow_users.add(self.user)
		self.client = Client()
		self.client.force_login(self.user)

	def testZeroAccount(self):
		''' Аккаунт без транзакций выдает сумму 0 '''
		# Given
		acc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		acc.allow_users.add(self.user)
		# When
		response = self.client.get('/account/%u' % acc.id)
		# Then
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf8')
		root = ElementTree.fromstring(text)
		self.assertEqual(int(root.find(".//total[@unit='RUB']").text), 0)

	def testCreditedAccount(self):
		''' На счет перечислены деньги '''
		# Given
		acc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		acc.allow_users.add(self.user)
		Transaction.objects.create(debit=self.oacc, credit=acc, amount=100, description='')
		# When
		response = self.client.get('/account/%u' % acc.id)
		# Then
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf8')
		root = ElementTree.fromstring(text)
		self.assertEqual(int(root.find(".//total[@unit='RUB']").text), 100)
		self.assertEqual(int(root.find(".//operation/income").text), 100)

	def testDebitAccount(self):
		''' Со счетасписаны  деньги '''
		# Given
		acc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		acc.allow_users.add(self.user)
		Transaction.objects.create(debit=acc, credit=self.oacc, amount=100, description='')
		# When
		response = self.client.get('/account/%u' % acc.id)
		# Then
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf8')
		root = ElementTree.fromstring(text)
		self.assertEqual(int(root.find(".//total[@unit='RUB']").text), -100)
		self.assertEqual(int(root.find(".//operation/outcome").text), 100)

	def testUserWithoutAccess(self):
		''' Пользователь без доступа к счету не может просматривать состояние счета '''
		# Given
		acc = Account.objects.create()
		# When
		response = self.client.get('/account/%u' % acc.id)
		# Then
		self.assertEqual(response.status_code, 403)
