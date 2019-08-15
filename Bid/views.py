from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from Property.models import Property
from .models import *
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_protect
from django.utils.encoding import python_2_unicode_compatible
from django.template import RequestContext
from django.core.urlresolvers import reverse
import datetime
# Create your views here.

@login_required
def bid(request,prop):
	ppt = Property.objects.get(pk = prop)
	bid = Bid.objects.filter(prop = ppt)
	if request.user == ppt.users:
		return render_to_response('ownbid.html', {'prop' : ppt, 'bid' : bid})
	if request.method == 'POST':
		form = IndiBid(request.POST)
		if form.is_valid():
			newprop = form.save(commit=False)
			newprop.user = request.user
			newprop.prop = ppt
			try:
				dup = Bid.objects.get(user = request.user, prop = ppt)
				dup.delete()
			except Bid.DoesNotExist:
				pass
			newprop.save()
#			url = reverse('/property/display', kwargs={'prop': prop})
		return HttpResponseRedirect('/bid/%s'%prop)
	else:
		form = IndiBid()
    	variables = RequestContext(request, {
    	'form' : form,
    	'user' : request.user,
    	'bids' : Bid.objects.filter(prop=ppt).order_by('value').reverse,
    	'prop' : ppt
    	})
    	return render_to_response(
    	'bid.html',
    	variables,
    	)

@login_required
def accept_bid(request, bid):
	bid_obj = Bid.objects.get(pk = bid)
	property_obj = bid_obj.prop
	ppt = Property.objects.get(pk = property_obj.id)
	latest_bid = Bid.objects.filter(prop = ppt).latest('time')
	hour_difference = datetime.datetime.now().hour - latest_bid.time.hour
	time_ellapsed = (latest_bid.time.year - datetime.datetime.now().year)*10000 + (latest_bid.time.month - datetime.datetime.now().month)*100 + latest_bid.time.day - datetime.datetime.now().day
	if time_ellapsed == 0 or (time_ellapsed == 1 and hour_difference < 24):
		return render_to_response('registration/wait.html')
	if ppt.users != request.user:
		return Http404("Access Denied")
	else:
		ppt.delete()
		return HttpResponseRedirect('/home')

@login_required
def bid_change(request, prop):
	new_price = request.GET['new_price']
	ppt=Property.objects.get(pk = prop)
	ppt.base_price = new_price
	ppt.save()
	return HttpResponseRedirect('/bid/%s'%prop)