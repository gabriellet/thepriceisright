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
FAILURE_TOLERANCE = -3
SUCCESS_TOLERANCE = 2

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
	def is_valid(self):
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

	def execute_sell(self, quantity, price):
		url   = ORDER.format(self.id, quantity, price)
		print url
		order = json.loads(urllib2.urlopen(url).read())
		return order

	def create_child(self, order, attempted_price):
		if (order['avg_price'] == 0):

			co = ChildOrder.objects.create(
				parent_order=self, 
				quantity = order['qty'],
				is_successful=False, 
				price=attempted_price
			)
		else:
			co = ChildOrder.objects.create(
				parent_order=self, 
				quantity = order['qty'],
				is_successful=True, 
				price=order['avg_price']
			)
		print "child created: "
		print co
		co.save()
		return co


	def trade(self):
		number_of_successes = 0
		maximum_child_size = self.quantity / 10  # hardcoded to split by 10%
		child_order_size = maximum_child_size
		quantity_to_sell = self.quantity

		while quantity_to_sell > 0:
			price = self.query_market_price() - ORDER_DISCOUNT
			if (quantity_to_sell < child_order_size):
				child_order_size = quantity_to_sell
			order = self.execute_sell(child_order_size, price)
			self.create_child(order, price)
			if (order['avg_price'] == 0):
				number_of_successes -= 1
			else:
				number_of_successes += 1
				# update quantity if successful
				quantity_to_sell -= order['qty']
			
			# Divide child order quantity into smaller chunks if
			# we hit the failure tolerance
			if (number_of_successes == FAILURE_TOLERANCE):
				child_order_size /= 2
				number_of_successes = 0
			# If child order succeeds at smaller quantities, sell
			# at a higher quantity
			elif (number_of_successes == SUCCESS_TOLERANCE and child_order_size < maximum_child_size):
				child_order_size *= 2
				number_of_successes = 0
			time.sleep(N)
<<<<<<< HEAD
=======
		# DONE!
		self.success = True
>>>>>>> leon





@python_2_unicode_compatible
class ChildOrder(models.Model):
	parent_order = models.ForeignKey(ParentOrder, on_delete=models.CASCADE)
	quantity = models.IntegerField(blank=False, default=0)
	is_successful = models.BooleanField(blank=False, default=False)
	price = models.FloatField(blank=False, default=0.0)
	time_executed = models.DateTimeField(blank=False, auto_now_add=True)

	def __str__(self):
		return "id: " + str(self.id) + " quantity: " + str(self.quantity) + " price: " + str(self.price) + " successful? " + str(self.is_successful)
