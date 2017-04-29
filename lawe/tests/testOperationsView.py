''' Operation tests '''
from xml.etree import ElementTree
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test import Client, TestCase
from lawe.models import Account, Transaction


class TestOperations(TestCase):
	''' Тестирование операций с применением API '''
	# @todo #70:15min Этот класс тестирует View, но называется некорректно
	#  и его надо как-то упорядочить с тем кассом, который идет ниже.
	#  Я его изначально неправильно назвал.
	#  Но возможно здесь не все относится к View
	def setUp(self):
		self.user = User.objects.create_user('john', 'password')
		self.client = Client()
		self.client.force_login(self.user)

	def testPageOk(self):
		''' Тестируем наличие url '''
		# Given
		# When
		response = self.client.get('/')
		# Then
		self.assertEqual(response.status_code, 200)

	def testPageContainLastOperation(self):
		''' Последняя введенная операция отображается в окне операций '''
		# Given
		a1 = Account.objects.create()
		a1.allow_users.add(self.user)
		a2 = Account.objects.create()
		a2.allow_users.add(self.user)
		Transaction.objects.create(debit=a1, credit=a2, amount=432, description='')
		# When
		response = self.client.get('/')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn('432', response.content.decode('utf8'))

	def testForbiddenCreditPost(self):
		''' Запрет создания операций, если нет доступа к счету дебета '''
		# Given
		a1 = Account.objects.create()
		a1.allow_users.add(self.user)
		a2 = Account.objects.create()
		# When
		response = self.client.post('/', {
			'date': 0,
			'debit_id': a1.id,
			'credit_id': a2.id,
			'amount': 1,
			'unit': 'RUB',
			'description': 'Проверка запрета'
		})
		# Then
		self.assertEqual(response.status_code, 403)

	def testForbiddenDebitPost(self):
		''' Запрет создания операций, если нет доступа к счету кредита '''
		# Given
		a1 = Account.objects.create()
		a2 = Account.objects.create()
		a2.allow_users.add(self.user)
		# When
		response = self.client.post('/', {
			'date': 0,
			'debit_id': a1.id,
			'credit_id': a2.id,
			'amount': 1,
			'unit': 'RUB',
			'description': 'Проверка запрета'
		})
		# Then
		self.assertEqual(response.status_code, 403)

	def testGrantedPost(self):
		''' Разрешение операций если есть доступ к обоим счетам '''
		# Given
		a1 = Account.objects.create()
		a1.allow_users.add(self.user)
		a2 = Account.objects.create()
		a2.allow_users.add(self.user)
		# When
		response = self.client.post('/', {
			'date': 0,
			'debit_id': a1.id,
			'credit_id': a2.id,
			'amount': 1,
			'unit': 'RUB',
			'description': 'Проверка разрешения'
		})
		# Then
		self.assertEqual(response.status_code, 200)

	def testHideUnaccessibleAccounts(self):
		''' В списке аккаунтов отображаются только разрешенные аккаунты '''
		# Given
		a1 = Account.objects.create(shortname='Enabled')
		a1.allow_users.add(self.user)
		Account.objects.create(shortname='Disabled')
		# When
		response = self.client.get('/')
		# Then
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf8')
		self.assertIn('Enabled', text)
		self.assertNotIn('Disabled', text)

	def testHideOperationWithDisabledAccounts(self):
		''' В списке операций отображаются только операции,
			где хотя бы один счет доступен '''
		# Given
		a1 = Account.objects.create()
		a1.allow_users.add(self.user)
		a2 = Account.objects.create()
		a3 = Account.objects.create()
		Transaction.objects.create(debit=a1, credit=a2, amount=1, description='Show')
		Transaction.objects.create(debit=a2, credit=a3, amount=1, description='Hide')
		# When
		response = self.client.get('/')
		# Then
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf8')
		self.assertIn('Show', text)
		self.assertNotIn('Hide', text)


class TestOperationsView(TestOperations):
	''' Тестирование того, что содержится в ответе сервера '''
	def setUp(self):
		''' Метод настройки '''
		super().setUp()
		self.a1 = Account.objects.create()
		self.a1.allow_users.add(self.user)
		self.a2 = Account.objects.create()
		self.a2.allow_users.add(self.user)

	def parse(self, response):
		''' Разор xml ответа от сервера '''
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf8')
		return ElementTree.fromstring(text)

	def testDefaultOperationUnitsIsRub(self):
		''' Единица измерения по умолчанию - рубли '''
		# Given
		Transaction.objects.create(debit=self.a1, credit=self.a2, amount=1, description='RUB')
		# When
		response = self.client.get('/')
		# Then
		root = self.parse(response)
		op = root.find(".//operation[description='RUB']")
		self.assertEqual(op.find('unit').text, 'RUB')

	def testOperationUnitsIsKg(self):
		''' Единица измерения - килограммы  '''
		# Given
		Transaction.objects.create(debit=self.a1, credit=self.a2, amount=1, description='KG', unit='KG')
		# When
		response = self.client.get('/')
		# Then
		root = self.parse(response)
		op = root.find(".//operation[description='KG']")
		self.assertEqual(op.find('unit').text, 'KG')

	def testOrderedByOpdata(self):
		''' Транзакции отображаются в порядке opdata '''
		# Given
		Transaction.objects.create(opdate=date.today(), debit=self.a1, credit=self.a2, amount=1)
		Transaction.objects.create(
			opdate=date.today() - timedelta(days=2),
			debit=self.a1,
			credit=self.a2,
			amount=2
		)
		# When
		response = self.client.get('/')
		# Then
		root = self.parse(response)
		self.assertEqual(int(root.find(".//operation[1]/amount").text), 1)
		self.assertEqual(int(root.find(".//operation[last()]/amount").text), 2)

	def testForHiddenAccountsInList(self):
		''' Не все аккаунты, используемые в операциях доступны в форме '''
		# Given
		a3 = Account.objects.create()
		Transaction.objects.create(opdate=date.today(), debit=self.a1, credit=a3, amount=1)
		# When
		response = self.client.get('/')
		# Then
		root = self.parse(response)
		self.assertEqual(int(root.find(".//account[@hidden]/id").text), a3.id)
