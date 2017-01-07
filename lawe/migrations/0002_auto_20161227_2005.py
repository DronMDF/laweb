# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-27 20:05
''' Миграция '''
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
	''' В Счетах поставил Date вместо DateTime и добавил описания '''
	dependencies = [
		('lawe', '0001_initial'),
	]

	operations = [
		migrations.AlterField(
			model_name='account',
			name='date',
			field=models.DateField(auto_now=True, verbose_name='Дата создания'),
		),
		migrations.AlterField(
			model_name='account',
			name='group',
			field=models.CharField(max_length=200, verbose_name='Основная группа'),
		),
		migrations.AlterField(
			model_name='account',
			name='name',
			field=models.CharField(max_length=200, verbose_name='Название'),
		),
		migrations.AlterField(
			model_name='account',
			name='shortname',
			field=models.CharField(max_length=50, verbose_name='Сокращенное название'),
		),
		migrations.AlterField(
			model_name='account',
			name='subgroup',
			field=models.CharField(max_length=200, verbose_name='Подгруппа'),
		),
		migrations.AlterField(
			model_name='account',
			name='unit',
			field=models.CharField(max_length=30, verbose_name='Измерение'),
		),
	]