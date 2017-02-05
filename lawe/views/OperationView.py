''' laweb views '''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from lawe.models import Account, Transaction


class OperationView(LoginRequiredMixin, TemplateView):
	''' Вьюв для операций '''
	template_name = 'operations.xml'
	content_type = 'application/xml'
	login_url = '/login/'

	def get_account_data(self, acc):
		''' Формирование контекста для аккаунта '''
		return {
			'id': acc.id,
			'name': acc.shortname
		}

	def get_operation_data(self, op):
		''' Формирование контекста для отдельной операции'''
		return {
			'date': op.date.strftime('%d.%m.%Y'),
			'debit': {
				'id': op.debit.id,
				'name': op.debit.shortname
			},
			'credit': {
				'id': op.credit.id,
				'name': op.credit.shortname
			},
			'amount': op.amount,
			'description': op.description
		}

	def get_context_data(self, **kwargs):
		''' Стандартный метод для формирования контекста '''
		context = super().get_context_data(**kwargs)
		context['accounts'] = [
			self.get_account_data(acc) for acc in Account.objects.all()
		]
		context['operations'] = [
			self.get_operation_data(op) for op in Transaction.objects.all().order_by(
				'-date'
			)
		]
		return context

	def post(self, request, *args, **kwargs):
		''' Обработчик вводимых операций '''
		debit = Account.objects.get(pk=request.POST['debit_id'])
		credit = Account.objects.get(pk=request.POST['credit_id'])
		Transaction.objects.create(debit=debit, credit=credit,
			amount=request.POST['amount'], description=request.POST['description'])
		return self.get(request, *args, **kwargs)
