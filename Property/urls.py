from django.conf.urls import url
from .views import *
#import Rating.urls
urlpatterns = [
    url(r'^$', register),
    url(r'^mapcoordinates/(?P<pid>[0-9]+)$', coordinates),
    url(r'^success/$', success),
    url(r'^all/$', all_prop),
    url(r'^search/',search),
    url(r'^display/(?P<propid>[0-9]+)$', displayProp),
 #   url(r'^regiseter/$', include(Register.urls)),
    ]