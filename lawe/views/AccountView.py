''' View для отчета по счету '''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from lawe.models import Account, Transaction


class AccountView(LoginRequiredMixin, TemplateView):
	''' Отчет по счету '''
	content_type = 'application/xml'
	login_url = '/login/'
	template_name = 'account.xml'

	def get_operation_context(self, op, acc):
		''' Контекст для одной операции '''
		opdate = op.opdate if op.opdate is not None else op.date
		return {
			'date': opdate.strftime('%d.%m.%Y'),
			'income': op.amount if op.credit == acc else '-',
			'outcome': op.amount if op.debit == acc else '-',
			'unit': op.unit,
			'description': op.description,
			'other': op.credit.shortname if op.debit == acc else op.debit.shortname
		}

	def getTotal(self, account, unit):
		''' Подсчет общего баланса для конкретной единицы измерения '''
		income = sum((t.amount for t in Transaction.objects.filter(credit=account, unit=unit)))
		outcome = sum((t.amount for t in Transaction.objects.filter(debit=account, unit=unit)))
		return income - outcome

	def get_context_data(self, **kwargs):
		''' Стандартный метод для формирования контекста '''
		context = super().get_context_data(**kwargs)
		account_id = kwargs['id']
		account = get_object_or_404(Account, pk=account_id)
		if not account.allow_users.filter(pk=self.request.user.id).exists():
			raise PermissionDenied
		context['shortname'] = account.shortname
		context['totals'] = [
			{
				'total': self.getTotal(account, unit),
				'unit': unit
			} for unit in ['RUB', 'KG']
		]
		context['operations'] = [
			self.get_operation_context(t, account) for t in Transaction.objects.filter(
				Q(credit=account) | Q(debit=account)
			).order_by('-opdate', '-date')
		]
		return context
