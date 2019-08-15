from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.template import RequestContext
from .models import *
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from Rating.models import Rating
from .forms import *
import operator

from geopy.geocoders import GoogleV3
from geopy.distance import vincenty

# Create your views here.

@login_required
def search(request):
	if request.method == 'POST':
		form = LocationSearch(request.POST)
		filters = Filters(request.POST)
		if form.is_valid() and filters.is_valid():
			searchlocation = form.cleaned_data['searchlocation']
			minAge = filters.cleaned_data['minAge']
			maxAge = filters.cleaned_data['maxAge']
			minBase = filters.cleaned_data['minBase']
			maxBase = filters.cleaned_data['maxBase']
			prop = Property.objects.filter(location = searchlocation,
age__gte=minAge, age__lte = maxAge,
base_price__gte = minBase, base_price__lte = maxBase)
			match = []
			req = ((form.cleaned_data['requirments']).replace(',',' ').replace('.',' ')).split(" ")
			i = 0
			for p in prop:
				t = 0
				description_of_property = (p.description).replace(',',' ').replace('.',' ').split(" ")
				for r in req:
					if r in description_of_property:
						t = t + 1
				t = t*100 + i 
				i = i + 1
				match.append(t)
			dicpair = dict( list( zip( match, prop)))
			sorted_dicpair = sorted(dicpair.items(), key = operator.itemgetter(1))
			geolocator = GoogleV3(timeout=10000)
			dist = []
			for p in prop:
				total_distance = 0
				p_cordinates = (p.latitude,p.longitude)
				for i in range (1,6):
					facility_cordinates = (request.POST['lat%s'%i],request.POST['lon%s'%i])
					total_distance = total_distance + vincenty(p_cordinates,facility_cordinates).meters
				dist.append(total_distance)
			distpair = dict( list( zip( match, prop)))
			sorted_distpair = sorted(dicpair.items(), key = operator.itemgetter(1))
			try:
				location = geolocator.geocode(searchlocation)
				lat = location.latitude
				lon = location.longitude
			except Exception:
				return render(request, 'property/search.html', {'form' : form,
				'filters' : filters,
				'list' : prop,
				'count' : prop.count(),
				'prop' : sorted_dicpair,
				'dist' : sorted_distpair,
				'lat' : 10.0158605,
				'long' : 76.3418666,
				'mag' : 1})
			return render(request, 'property/search.html', {'form' : form,
				'filters' : filters,
				'list' : prop,
				'count' : prop.count(),
				'prop' : sorted_dicpair,
				'dist' : sorted_distpair,
				'lat' : lat,
				'long' : lon,
				'mag' : 15})
		else:
			return render(request, 'property/search.html', {'form' : form,'filters' : filters})
	else:
		form = LocationSearch()
		filters = Filters()
		return render(request, 'property/search.html', {'form' : form, 'filters' : filters})

@login_required
def register(request):
	if request.method == 'POST':
		form = Prop(request.POST)
		if form.is_valid():
			newprop = form.save(commit = False)
			newprop.users = request.user
			newprop.final_rating = 0
			newprop.save()
			pid = newprop.id
		return HttpResponseRedirect('mapcoordinates/%s'%pid)
	else:
		form = Prop()
    	variables = RequestContext(request, {
    	'form': form,
    	'user': request.user.username
    	})
    	return render_to_response(
    	'regi_prop.html',
    	variables,
    	)

def coordinates(request, pid):
	ppt = Property.objects.get(pk = pid)
	if request.method == 'POST':
		ppt.latitude = request.POST['latitude']
		ppt.longitude = request.POST['longitude']
		ppt.save()
		return HttpResponseRedirect('/property/success')
	else:
		geolocator = GoogleV3(timeout=1000)	
		try:
			location = geolocator.geocode(ppt.location)
			lat = location.latitude
			lon = location.longitude
		except Exception:
			return render(request, 'registration/propertycordinates.html', {				'prop' : ppt,
				'lat' : 10.0158605,
				'long' : 76.3418666,
				'mag' : 1})
		context={'prop' : ppt,
				'lat' : lat,
				'long' : lon,
				'mag' : 18}
		return render(request, 'registration/propertycordinates.html', context)

def success(request):
	return render_to_response(
    'prop_success.html',
    )

def all_prop(request):
	prop_list = Property.objects.all()
	context = {'list' : prop_list}
	return render(request, 'proplist.html', context)

def displayProp(request, propid):
	try:
		prop = Property.objects.get(pk = propid)
		prop_details = model_to_dict(prop,exclude = ['id','users'])
		users = User.objects.get(pk = prop.users.id)
		reviews = Rating.objects.filter(prop = propid)
	except Property.DoesNotExist:
		raise Http404("Property not found")
	except Rating.DoesNotExist:
		return render(request, 'property/propdisplay.html', {'prop':prop, 'prop_details': prop_details, 'users': users})
	return render(request, 'property/propdisplay.html', {'prop':prop, 'prop_details': prop_details, 'users': users,'reviews': reviews})