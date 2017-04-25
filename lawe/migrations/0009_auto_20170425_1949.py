# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-25 19:49
''' Добавляем новое поле с датой проведения '''

from __future__ import unicode_literals

from django.db import migrations, models


def init_opdate(apps, schema_editor):
	''' Заполняем opdate значениями из date '''
	Transaction = apps.get_model("lawe", "Transaction")
	db_alias = schema_editor.connection.alias
	for op in Transaction.objects.using(db_alias).all():
		op.opdate = op.date
		op.save()


class Migration(migrations.Migration):
	''' Миграция '''
	dependencies = [
		('lawe', '0008_auto_20170425_1839'),
	]

	operations = [
		migrations.AddField(
			model_name='transaction',
			name='opdate',
			field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата проведения'),
		),
		migrations.AlterField(
			model_name='transaction',
			name='date',
			field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания'),
		),
		migrations.RunPython(init_opdate),
	]
