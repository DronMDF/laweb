''' Models '''
from django.db import models


class Account(models.Model):
	''' Счет '''
	date = models.DateField('Дата создания', auto_now=True)
	group = models.CharField('Основная группа', max_length=200)
	subgroup = models.CharField('Подгруппа', max_length=200)
	name = models.CharField('Название', max_length=200)
	shortname = models.CharField('Сокращенное название', max_length=50)
	unit = models.CharField('Измерение', max_length=30)


class Transaction(models.Model):
	''' Операции '''
	date = models.DateTimeField('date')
	debit = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
	credit = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
	amount = models.IntegerField()
	description = models.CharField(max_length=200)
