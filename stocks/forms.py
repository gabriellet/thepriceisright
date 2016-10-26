from django import forms
from models import ParentOrder


class ParentOrderForm(forms.Form):
	class Meta:
		model = ParentOrder
		fields = ('is_sell', 'quantity')