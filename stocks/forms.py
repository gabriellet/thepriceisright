from django import forms

class TradeForm(forms.Form):
	qty = forms.IntegerField(label='Quantity', 
		widget=forms.NumberInput(attrs={'class': 'form-control', 'name': 'qty'}))