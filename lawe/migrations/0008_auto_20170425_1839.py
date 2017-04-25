# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-25 18:39
''' Изменили формат сохранения времени '''

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
	''' Миграция формата обновления времени '''
	dependencies = [
		('lawe', '0007_auto_20170423_1937'),
	]

	# pylint не умеет локально дисейблить duplicate-code, а надо
	operations = [
		migrations.AlterField(
			model_name='transaction',
			name='date',
			field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
		),
	]
