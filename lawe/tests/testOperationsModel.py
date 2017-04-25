''' Тестирование модели операций '''
from django.test import TestCase
from lawe.models import Account, Transaction


class TestOperationsModel(TestCase):
	''' Тестируем модель '''
	def testAutotimeOnCreation(self):
		''' При обновлении модели дата не должна меняться '''
		# Given
		op = Transaction.objects.create(
			debit=Account.objects.create(),
			credit=Account.objects.create(),
			amount=1
		)
		date1 = op.date
		# When
		op.save()
		# Then
		self.assertEqual(date1, op.date)
