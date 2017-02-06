""" laweb URL Configuration """
from django.conf.urls import url, include
from django.contrib import admin
from lawe.views import AccountView, OperationView

urlpatterns = [
	url(r'^$', OperationView.as_view()),
	url(r'^account/(?P<id>[0-9]+)/?$', AccountView.as_view()),
	url(r'^admin/', admin.site.urls),
	url('^', include('django.contrib.auth.urls'))
]
