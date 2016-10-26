from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
import urllib2
import time
import json


QUERY = "http://localhost:8080/query?id={}"
ORDER = "http://localhost:8080/order?id={}&side=sell&qty={}&price={}"
ORDER_DISCOUNT = 10
N = 5

# Create your models here.
@python_2_unicode_compatible
class ParentOrder(models.Model):
	quantity = models.IntegerField(blank=False, default=0)
	stock_type = models.CharField(max_length=20)
	is_sell = models.BooleanField(blank=False, default=True)
	time_executed = models.DateTimeField(blank=False, auto_now_add=True)
	success = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	# checks if quantity is positive
	def valid_order(self):
		if self.quantity < 0:
			return False
		else:
			return True

	def __str__(self):
		return str(self.id) + ": " + str(self.quantity) + " x " + self.stock_type

	def query_market_price(self):
		quote = json.loads(urllib2.urlopen(QUERY.format(self.id)).read())
		price = float(quote['top_bid']['price'])
		print "Quoted at %s" % price
		return price

	def trade(self):
		number_of_successes = 0
		maximum_child_size = self.quantity / 10  # hardcoded to split by 10%

		





@python_2_unicode_compatible
class ChildOrder(models.Model):
	parent_order = models.ForeignKey(ParentOrder, on_delete=models.CASCADE)
	quantity = models.IntegerField(blank=False, default=0)
	is_successful = models.BooleanField(blank=False, default=False)
	price = models.FloatField(blank=False, default=0.0)
	time_executed = models.DateTimeField(blank=False, auto_now_add=True)

	def __str__(self):
		return str(self.id) + ": " + str(self.quantity)
