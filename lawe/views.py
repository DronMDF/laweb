''' laweb views '''
from django.views.generic import TemplateView


class OperationView(TemplateView):
	''' Вьюв для операций '''
	template_name = 'operations.xml'
	context_type = 'application/xml'
