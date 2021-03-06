''' Models '''
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
	''' Счет '''
	date = models.DateField('Дата создания', auto_now=True)
	group = models.CharField('Основная группа', max_length=200, blank=True)
	subgroup = models.CharField('Подгруппа', max_length=200, blank=True)
	name = models.CharField('Название', max_length=200, blank=True)
	shortname = models.CharField('Сокращенное название', max_length=50)
	allow_users = models.ManyToManyField(User)

	class Meta:
		''' Метаданные счетов '''
		verbose_name = 'Счет'
		verbose_name_plural = 'Счета'
		ordering = ['shortname']

	def __str__(self):
		return self.shortname


class Transaction(models.Model):
	''' Операции '''
	UNIT_CHOICES = (
		('RUB', 'руб'),
		('KG', 'кг')
	)

	date = models.DateTimeField('Дата и время создания', auto_now_add=True)
	opdate = models.DateField('Дата проведения', null=True)
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
	unit = models.CharField('Ед. изм.', max_length=3, choices=UNIT_CHOICES, default='RUB')
	description = models.CharField('Описание', max_length=200, blank=True)

	class Meta:
		''' Метаданные операций '''
		verbose_name = 'Операция'
		verbose_name_plural = 'Операции'
