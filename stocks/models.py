from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
import urllib2
import datetime
import time
import json


QUERY = "http://localhost:8080/query?id={}"
ORDER = "http://localhost:8080/order?id={}&side=sell&qty={}&price={}"
ORDER_DISCOUNT = 1
N = 5
FAILURE_TOLERANCE = -3
SUCCESS_TOLERANCE = 2

# Create your models here.
@python_2_unicode_compatible
class ParentOrder(models.Model):
	quantity = models.IntegerField(blank=False, default=1)
	stock_type = models.CharField(max_length=20)
	is_sell = models.BooleanField(blank=False, default=True)
	time_executed = models.DateTimeField(blank=False, auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	IN_PROGRESS = 'P'
	COMPLETED = 'C'
	FAILED = 'F'
	STATUS_CHOICES = (
		(IN_PROGRESS, 'In Progress'),
		(COMPLETED, 'Completed'),
		(FAILED, 'Failed')	
	)

	status = models.CharField(
		max_length=1,
		choices=STATUS_CHOICES,
		default=IN_PROGRESS
	)

	
	# checks if quantity is positive
	def is_valid(self):
		if self.quantity <= 0:
			return False
		else:
			return True

	def verify_market_price(self, price_json):
		top_bid = price_json.get('top_bid')
		if top_bid is None:
			return False
		price = top_bid.get('price')
		if price is None:
			return False
		return True


	def __str__(self):
		return str(self.id) + ": " + str(self.quantity) + " x " + self.stock_type + ' status:' + self.status

	def query_market_price(self, number_of_tries=10):
		quote = json.loads(urllib2.urlopen(QUERY.format(self.id)).read())
		while not self.verify_market_price(quote):  # We failed to verify, the exchange simulator returned a bad response
			quote = json.loads(urllib2.urlopen(QUERY.format(self.id)).read())
			time.sleep(5)  # sleep 5 seconds before trying again
			number_of_tries -= 1
			if number_of_tries == 0:  # no tries left, we give up querying and selling
				return False
		price = float(quote['top_bid']['price'])
		print "Quoted at %s" % price
		return price

	def execute_sell(self, quantity, price):
		url   = ORDER.format(self.id, quantity, price)
		response = urllib2.urlopen(url).read()
		if response == "":
			order = {
			u'timestamp': datetime.datetime.now(), 
			u'qty': child_order_size, 
			u'side': u'sell', 
			u'avg_price': 0.0
			}
		else:
			order = json.loads(response)
		return order

	def create_child(self, order, attempted_price):
		if (order['avg_price'] == 0.0):

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

	def get_progress(self):
		return

	def trade(self):
		if not self.is_valid():
			print "Problem, someone created a bad parent order that shouldn't even be here"
			return  # This code should never be reached, since if an order is not valid, we don't even create it

		number_of_successes = 0
		if ((self.quantity/10) < 10):
			maximum_child_size = self.quantity
		else:
			maximum_child_size = self.quantity / 10  # hardcoded to split by 10%
		child_order_size = maximum_child_size
		quantity_to_sell = self.quantity

		while quantity_to_sell > 0:
			price = self.query_market_price() 
			if price is False:
				self.status = self.FAILED
				self.save()
				return
			price -= ORDER_DISCOUNT  # query is successful, update price accordingly
			if (quantity_to_sell < child_order_size):
				child_order_size = quantity_to_sell  # make sure child order size never exceeds what we have left to sell
			order = self.execute_sell(child_order_size, price)

			self.create_child(order, price)

			# logic for handling failure to sell
			if (order['avg_price'] == 0.0):
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

			# sleep for N seconds before selling again
			time.sleep(N)

		# DONE with while loop!
		self.status = self.COMPLETED
		self.save() # we forgot to save after setting self.success=True. The update() function solves this

@python_2_unicode_compatible
class ChildOrder(models.Model):
	parent_order = models.ForeignKey(ParentOrder, on_delete=models.CASCADE)
	quantity = models.IntegerField(blank=False, default=0)
	is_successful = models.BooleanField(blank=False, default=False)
	price = models.FloatField(blank=False, default=0.0)
	time_executed = models.DateTimeField(blank=False, auto_now_add=True)

	def __str__(self):
		return "id: " + str(self.id) + " quantity: " + str(self.quantity) + " price: " + str(self.price) + " successful? " + str(self.is_successful)
