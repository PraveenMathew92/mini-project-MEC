from __future__ import unicode_literals
from django.forms import ModelForm
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.
class Property(models.Model):
	address = models.CharField(max_length = 100, blank = False, null = False)
	location = models.CharField(max_length = 20, blank = False, null = False)
	age = models.IntegerField()
	base_price = models.IntegerField()
	description = models.TextField()
	users = models.ForeignKey(User, on_delete = models.CASCADE)
	final_rating = models.FloatField(blank = False, null = True)
	latitude = models.FloatField(null = True)
	longitude = models.FloatField(null = True)
	def __str__(self):
		return '%s \t %s'%(self.address, self.users)


class Prop(ModelForm):
    class Meta:
        model = Property
        #fields = '__all__'
        exclude = ['users', 'final_rating', 'latitude', 'longitude']