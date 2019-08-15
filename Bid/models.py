from __future__ import unicode_literals
from Property.models import Property
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.
class Bid(models.Model):
	value = models.IntegerField()
	time = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	prop = models.ForeignKey(Property,on_delete=models.CASCADE)
	def __str__(self):
		return '%d \t %s \t %s' % (self.value, self.user, self.prop)


class IndiBid(ModelForm):
	class Meta:
		model = Bid
		fields = ['value']