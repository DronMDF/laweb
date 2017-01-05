''' laweb views '''
from django.views.generic import TemplateView
from lawe.models import Transaction


class OperationView(TemplateView):
	''' Вьюв для операций '''
	template_name = 'operations.xml'
	context_type = 'application/xml'

	def get_operation_data(self, op):
		''' Формирование контекста для отдельной операции'''
		return {
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
		context['operations'] = [
			self.get_operation_data(op) for op in Transaction.objects.all()
		]
		return context
