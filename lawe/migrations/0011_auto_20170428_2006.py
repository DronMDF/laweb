# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-28 20:06
''' Миграция '''
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
	''' Сокращаем название единиц измерения '''
	dependencies = [
		('lawe', '0010_auto_20170425_2000'),
	]

	operations = [
		migrations.AlterModelOptions(
			name='account',
			options={
				'ordering': ['shortname'],
				'verbose_name': 'Счет',
				'verbose_name_plural': 'Счета'
			},
		),
		migrations.AlterField(
			model_name='transaction',
			name='unit',
			field=models.CharField(
				choices=[('RUB', 'руб'), ('KG', 'кг')],
				default='RUB',
				max_length=3,
				verbose_name='Ед. изм.'
			),
		),
	]