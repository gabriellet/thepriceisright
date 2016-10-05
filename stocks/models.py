from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class User(models.Model):
	username = models.CharField(max_length=80)
	password = models.CharField(max_length=80)
	def __str__(self):
		return self.username

@python_2_unicode_compatible
class ParentOrder(models.Model):
	quantity = models.IntegerField(default=0)
	stock_type = models.CharField(max_length=20)
	is_sell = models.BooleanField(default=True)
	time_executed = models.DateTimeField(auto_now=False, auto_now_add=True)
	order_id = models.AutoField(primary_key=True)
	# def __str__(self):
	# 	return self.stock_type
	def __str__(self):
		return str(self.order_id) + ": " + str(self.quantity) + "x" + self.stock_type

@python_2_unicode_compatible
class ChildOrder(models.Model):
	order_id =models.ForeignKey(ParentOrder, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	is_successful = models.BooleanField(default=False)
	price = models.FloatField(default=0.0)
	def __str__(self):
		return str(self.id) + ": " + str(self.quantity)
