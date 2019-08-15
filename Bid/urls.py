from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^(?P<prop>[0-9]+)$', bid),
	url(r'^(?P<prop>[0-9]+)/change', bid_change),
	url(r'^accept/(?P<bid>[0-9]+)$', accept_bid)
]