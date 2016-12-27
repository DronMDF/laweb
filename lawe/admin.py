''' Администрирование через админку.

Только часть ресурсов доступны для редактирования здесь.
Возможно со временем админка вообще отомрет.
Но пока так проще.
'''

from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
	''' Админка для счетов '''
	list_display = ('group', 'subgroup', 'name')
