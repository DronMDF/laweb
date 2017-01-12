''' View для отчета по счету '''
from django.views.generic import TemplateView


class AccountView(TemplateView):
	''' Отчет по счету '''
	template_name = 'account.xml'
	content_type = 'application/xml'

	def get_context_data(self, **kwargs):
		''' Стандартный метод для формирования контекста '''
		context = super().get_context_data(**kwargs)
		context['total'] = 0
		return context
