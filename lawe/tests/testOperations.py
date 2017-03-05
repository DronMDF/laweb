''' Operation tests '''
from django.contrib.auth.models import User
from django.test import Client, TestCase
from lawe.models import Account, Transaction


class TestOperations(TestCase):
	''' Тестирование операций с применением API '''
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
		a1 = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		a2 = Account.objects.create(group='G', subgroup='E', name='NN', shortname='SN',
				unit='тр')
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
			'debit_id': a1.id,
			'credit_id': a2.id,
			'amount': 1,
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
			'debit_id': a1.id,
			'credit_id': a2.id,
			'amount': 1,
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
			'debit_id': a1.id,
			'credit_id': a2.id,
			'amount': 1,
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
		text = response.content.decode('utf8')
		self.assertIn('Enabled', text)
		self.assertNotIn('Disabled', text)
