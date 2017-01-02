''' Operation tests '''
from django.test import Client, TestCase


class TestOperations(TestCase):
	''' Тестирование операций с применением API '''
	def testPageOk(self):
		''' Тестируем наличие url '''
		# Given
		# When
		response = Client().get('/')
		# Then
		self.assertEqual(response.status_code, 200)
