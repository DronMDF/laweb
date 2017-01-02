''' Operation tests '''
from django.test import Client, TestCase
from lawe.models import Account, Transaction


class TestOperations(TestCase):
	''' Тестирование операций с применением API '''
	def testPageOk(self):
		''' Тестируем наличие url '''
		# Given
		# When
		response = Client().get('/')
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
		response = Client().get('/')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn('432', response.content.decode('utf8'))
