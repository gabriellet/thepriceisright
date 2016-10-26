from django import forms

from models import ParentOrder


class ParentOrderForm(forms.ModelForm):
	class Meta:
		model = ParentOrder
		fields = ('quantity',)