''' laweb views '''
from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView
from lawe.models import Account, Transaction


class OperationView(LoginRequiredMixin, TemplateView):
	''' Вьюв для операций '''
	content_type = 'application/xml'
	login_url = '/login/'
	template_name = 'operations.xml'

	def get_account_data(self, acc):
		''' Формирование контекста для аккаунта '''
		return {
			'id': acc.id,
			'name': acc.shortname,
			'hidden': not acc.allow_users.filter(pk=self.request.user.id).exists()
		}

	def get_operation_data(self, op):
		''' Формирование контекста для отдельной операции'''
		opdate = op.opdate if op.opdate is not None else op.date
		# @todo #77:15min Необходимо убрать лишнюю информацию по debit/credit из контекста
		#  Необходим только debit_id/credit_id, a остальная информация находится в списке аккаунтов.
		return {
			'id': op.id,
			'timestamp': op.date.timestamp(),
			'date': opdate.strftime('%d.%m.%Y'),
			'debit': {
				'id': op.debit.id,
				'name': op.debit.shortname
			},
			'credit': {
				'id': op.credit.id,
				'name': op.credit.shortname
			},
			'amount': op.amount,
			'unit': op.unit,
			'description': op.description
		}

	def date(self, delta):
		''' Форматирует дату в соответствии с нужным форматом '''
		day = date.today() - timedelta(days=delta)
		return {
			'id': delta,
			'date': day.strftime('%d.%m.%Y')
		}

	def get_context_data(self, **kwargs):
		''' Стандартный метод для формирования контекста '''
		context = super().get_context_data(**kwargs)

		context['dates'] = [self.date(delta) for delta in [4, 3, 2, 1, 0]]

		# @todo #77:15min необходимо достать номер страницы из параметров запроса.
		#  Не знаю, как оставаться на нужной странице в процессе POST,
		#  но при обычных запросах это должно нормально показываться.
		operations = Paginator(
			Transaction.objects.filter(
				Q(debit__allow_users__id=self.request.user.id) |
				Q(credit__allow_users__id=self.request.user.id)
			).distinct().order_by('-opdate', '-date'),
			100
		)
		context['operations'] = [self.get_operation_data(op) for op in operations.page(1)]

		# @todo #77:15min Необходимо передать данные страницы в контекст,
		#  чтобы можно было сгенерировать навигацию по страницам.

		# @todo #77:15min Фильтровать передаваемые аккаунты необходимо с помощью Query.
		#  Сейчас мы имеем неоптимальное извлечение информации с анализом каждой записи.
		used_debit_acc = {o['debit']['id'] for o in context['operations']}
		used_credit_acc = {o['credit']['id'] for o in context['operations']}
		used_acc = used_debit_acc | used_credit_acc
		context['accounts'] = [
			self.get_account_data(acc)
			for acc in Account.objects.all()
			if any((
				acc.allow_users.filter(pk=self.request.user.id).exists(),
				acc.id in used_acc
			))
		]
		return context

	# @todo #57:30min Можно создать операцию с одним и тем же счетом
	#  баланс счета при этом не изменится, потому что он будет сразу и дебетом и кредитом
	def post(self, request, *args, **kwargs):
		''' Обработчик вводимых операций '''
		opdate = date.today() - timedelta(days=int(request.POST['date']))
		debit = Account.objects.get(pk=request.POST['debit_id'])
		credit = Account.objects.get(pk=request.POST['credit_id'])
		permit = all((
			debit.allow_users.filter(pk=self.request.user.id).exists(),
			credit.allow_users.filter(pk=self.request.user.id).exists()
		))
		if not permit:
			raise PermissionDenied
		Transaction.objects.create(
			opdate=opdate,
			debit=debit,
			credit=credit,
			amount=request.POST['amount'],
			unit=request.POST['unit'],
			description=request.POST['description']
		)
		return self.get(request, *args, **kwargs)
