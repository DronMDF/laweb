from django.db import models


class Account(models.Model):
	date = models.DateTimeField('Creation date')
	group = models.CharField(max_length=200)
	subgroup = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	shortname = models.CharField(max_length=50)
	unit = models.CharField(max_length=30)


class Transaction(models.Model):
	date = models.DateTimeField('date')
	debit = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
	credit = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
	amount = models.IntegerField()
	description = models.CharField(max_length=200)
