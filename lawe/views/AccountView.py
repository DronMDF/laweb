''' View для отчета по счету '''
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from lawe.models import Account, Transaction


class AccountView(TemplateView):
	''' Отчет по счету '''
	template_name = 'account.xml'
	content_type = 'application/xml'

	def get_operation_context(self, op, acc):
		''' Контекст для одной операции '''
		return {
			'date': op.date.strftime('%d.%m.%Y'),
			'income': op.amount if op.credit == acc else '-',
			'outcome': op.amount if op.debit == acc else '-',
			'description': op.description,
			'other': op.credit.shortname if op.debit == acc else op.debit.shortname
		}

	def get_context_data(self, **kwargs):
		''' Стандартный метод для формирования контекста '''
		context = super().get_context_data(**kwargs)
		account_id = kwargs['id']
		account = get_object_or_404(Account, pk=account_id)
		income = sum((t.amount for t in Transaction.objects.filter(credit=account)))
		outcome = sum((t.amount for t in Transaction.objects.filter(debit=account)))
		context['total'] = income - outcome
		context['operations'] = [
			self.get_operation_context(t, account) for t in Transaction.objects.filter(
				Q(credit=account) | Q(debit=account)
			).order_by('-date')
		]
		return context
