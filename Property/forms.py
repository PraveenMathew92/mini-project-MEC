import re
from django import forms
from .models import Property
from django.utils.translation import ugettext_lazy as _

class LocationSearch(forms.Form):
	searchlocation = forms.CharField( 
        widget = forms.TextInput(attrs = dict
        (required = True, max_length = 30)),
        label = _("Search Location"))
	requirments = forms.CharField(#regex=r'^\w+$',
		required = False,
        widget = forms.TextInput(attrs = dict
        (required = False, max_length = 30)),
        label = _("Property Requirments"))

	def clean_searchlocation(self):
		if Property.objects.filter(location=self.cleaned_data['searchlocation']).exists():
			#self.cleaned_data['searchlocation']
			return self.cleaned_data['searchlocation']
		else:
			raise forms.ValidationError(_("Sorry, No Properties are available in that location "))

class Filters(forms.Form):
	minAge = forms.IntegerField(
		required = False,
        label = _("Minumum Age"),
        initial = '1')
	maxAge = forms.IntegerField(
		required = False,
        label = _("Maxmimum Age"),
        initial = '999')
	minBase = forms.IntegerField(
		required = False,
		label = _("Minimum Price"),
		initial = '1')
	maxBase = forms.IntegerField(
		required = False,
		label = _("Maximum Price"),
		initial = '99999999999')


	def clean(self):
		if 'minAge' in self.cleaned_data or 'maxAge' in self.cleaned_data:
			if self.cleaned_data['minAge'] > self.cleaned_data['maxAge']:
				raise forms.ValidationError(_("Enter valid data."))
		if 'minBase' in self.cleaned_data or 'maxBase' in self.cleaned_data:
			if self.cleaned_data['minBase'] > self.cleaned_data['maxBase']:
				raise forms.ValidationError(_("Enter valid data."))
		return self.cleaned_data