""" laweb URL Configuration """
from django.conf.urls import url
from django.contrib import admin
from lawe.views import OperationView

urlpatterns = [
	url('', OperationView.as_view()),
	url(r'^admin/', admin.site.urls),
]
