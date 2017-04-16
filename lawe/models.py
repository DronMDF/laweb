''' Models '''
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
	''' Счет '''
	date = models.DateField('Дата создания', auto_now=True)
	group = models.CharField('Основная группа', max_length=200)
	subgroup = models.CharField('Подгруппа', max_length=200)
	name = models.CharField('Название', max_length=200)
	shortname = models.CharField('Сокращенное название', max_length=50)
	unit = models.CharField('Измерение', max_length=30)
	allow_users = models.ManyToManyField(User)

	class Meta:
		''' Метаданные счетов '''
		verbose_name = 'Счет'
		verbose_name_plural = 'Счета'

	def __str__(self):
		return self.shortname


class Transaction(models.Model):
	''' Операции '''
	date = models.DateTimeField('Дата', auto_now=True)
	debit = models.ForeignKey(
		Account,
		verbose_name='Дебет',
		on_delete=models.CASCADE,
		related_name='+'
	)
	credit = models.ForeignKey(
		Account,
		verbose_name='Кредит',
		on_delete=models.CASCADE,
		related_name='+'
	)
	amount = models.IntegerField('Сумма')
	description = models.CharField('Описание', max_length=200)

	class Meta:
		''' Метаданные операций '''
		verbose_name = 'Операция'
		verbose_name_plural = 'Операции'
