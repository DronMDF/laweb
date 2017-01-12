''' Тесты для страницы отчета по счету '''
from django.test import Client, TestCase
from lawe.models import Account


class TestAccountView(TestCase):
	''' Тестирование AccountView '''
	def testZeroAccount(self):
		''' Аккаунт без транзакций выдает сумму 0 '''
		# Given
		acc = Account.objects.create(group='G', subgroup='E', name='N', shortname='S',
				unit='тр')
		# When
		response = Client().get('/account/%u' % acc.id)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn('<total>0</total>', response.content.decode('utf8'))
