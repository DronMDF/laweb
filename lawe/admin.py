''' Администрирование через админку.

Только часть ресурсов доступны для редактирования здесь.
Возможно со временем админка вообще отомрет.
Но пока так проще.
'''

from django.contrib import admin
from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
	''' Админка для счетов '''
	list_display = ('shortname', 'group', 'subgroup', 'name')
	list_filter = ('group',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	''' Админка для операций '''
	list_display = ('date', 'debit', 'credit', 'amount', 'unit', 'description')
	list_filter = ('debit', 'credit', 'unit')
